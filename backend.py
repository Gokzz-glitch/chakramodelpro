import html
import json
import os
import subprocess
import sys
import threading
import tempfile
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse

ROOT = Path(__file__).resolve().parent
PORT = int(os.environ.get("PORT", "8000"))
MODEL_ROOT = ROOT
JOBS = {}
JOBS_LOCK = threading.Lock()
MODELS = {
    "pranet": {"label": "PraNet-V1 (Res2Net50)", "engine": "segmentation", "script": ROOT / "models" / "pranet_v1" / "evaluate_pranetv1_polypgen_full.py", "weights": ROOT / "models" / "pranet_v1" / "weights.pth", "lib_parent": ROOT / "models" / "pranet_v1"},
    "pvt": {"label": "PVT-PraNet-V1 (PVTv2-B2)", "engine": "segmentation", "script": ROOT / "models" / "pvt_pranet_v1" / "evaluate_pvt_pranetv1_polypgen_full.py", "weights": ROOT / "models" / "pvt_pranet_v1" / "weights.pth", "lib_parent": ROOT / "models" / "pvt_pranet_v1"},
    "yolo": {"label": "YOLO (root yolo_best.pt)", "engine": "yolo", "weights": ROOT / "models" / "yolo_root" / "weights.pt", "lib_parent": ROOT / "models" / "yolo_root"},
    "vit": {"label": "YOLOViT (VIT.pt)", "engine": "yolo", "weights": ROOT / "models" / "yolovit_vit" / "weights.pt", "lib_parent": ROOT / "models" / "yolovit_vit"},
    "yolovit": {"label": "YOLOViT (yolo_best.pt)", "engine": "yolo", "weights": ROOT / "models" / "yolovit_yolo" / "weights.pt", "lib_parent": ROOT / "models" / "yolovit_yolo"},
    "chakra": {"label": "ChakraNet (AdaBN PraNet-ResNet101)", "engine": "unsupported", "weights": ROOT / "models" / "chakranet" / "weights.pth", "lib_parent": ROOT / "models" / "chakranet"},
}


def page(message="", job_id=""):
    options = "".join(f'<option value="{key}">{html.escape(config["label"])}</option>' for key, config in MODELS.items())
    model_config = json.dumps({key: {name: str(value) for name, value in config.items() if name in ("weights", "lib_parent", "engine")} for key, config in MODELS.items()})
    notice = f'<p class="status">Job <code>{html.escape(job_id)}</code> started. <a href="/jobs/{html.escape(job_id)}">View status</a></p>' if job_id else ""
    if message:
        notice = f'<p class="error">{html.escape(message)}</p>'
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Polyp evaluation</title>
<style>body{{font:16px system-ui,sans-serif;max-width:850px;margin:40px auto;padding:0 20px;background:#f5f7fa;color:#18212b}}main{{background:white;padding:28px;border:1px solid #dce3ea;border-radius:10px}}h1{{margin-top:0}}form{{display:grid;gap:14px}}label{{display:grid;gap:6px;font-weight:600}}input,select{{font:inherit;padding:10px;border:1px solid #b8c4cf;border-radius:6px}}button{{font:inherit;padding:11px 16px;background:#146c94;color:white;border:0;border-radius:6px;cursor:pointer}}small{{font-weight:400;color:#5e6a75}}.status{{padding:12px;background:#e8f5ec}}.error{{padding:12px;background:#fff0f0;color:#a12626}}</style></head>
<body><main><h1>Polyp evaluation</h1><p>Choose a model and enter the server-side directories used by the evaluator.</p>{notice}
<form method="post" action="/run">
<label>Google Drive mount<select id="mount_root" name="mount_root"><option value="">Detecting mounted drives...</option></select><small id="mount_status">Checking local Drive mounts</small></label>
<label>Model<select name="model">{options}</select></label>
<label>Input type<select name="source" id="source" onchange="toggleSource()"><option value="dataset">Dataset directory</option><option value="video">Video from directory</option></select></label>
<div id="datasetFields"><label>Dataset directory<small>Directories discovered under the model root</small><select id="dataset" name="dataset" required><option value="">Loading directories...</option></select></label></div>
<div id="videoFields" hidden><label>Video directory<small>Videos are loaded from this server-side directory</small><input id="video_dir" name="video_dir" value="I:\\My Drive\\colon cancer\\colon_cancer_dataset\\videos with polyps" placeholder="/kaggle/input/videos"></label><label>Video file<select id="video" name="video"><option value="">Enter a video directory first</option></select></label></div>
<label>Weights file<input id="weights" name="weights" required placeholder="/kaggle/input/model/model.pth"></label>
<label>Library parent<small>Folder containing the model repository's lib directory</small><input id="lib_parent" name="lib_parent" required placeholder="/kaggle/input/binary_seg"></label>
<label>Output directory<input name="out" value="I:\\My Drive\\colon cancer\\outputs" required placeholder="/kaggle/working/evaluation"></label>
<label>Device<select name="device"><option value="cuda" selected>CUDA GPU</option><option value="cpu">CPU</option></select></label>
<label>Threshold<input name="thresh" type="number" min="0" max="1" step="0.01" value="0.5"></label>
<button type="submit">Start evaluation</button></form>
<script>
const modelConfig = {model_config};
function updateModel() {{ const config = modelConfig[document.querySelector('[name=model]').value]; document.getElementById('weights').value = config.weights; document.getElementById('lib_parent').value = config.lib_parent; }}
function toggleSource() {{ const video = document.getElementById('source').value === 'video'; document.getElementById('datasetFields').hidden = video; document.getElementById('videoFields').hidden = !video; document.querySelector('[name=dataset]').required = !video; document.getElementById('video_dir').required = video; document.getElementById('video').required = video; }}
async function loadVideos() {{ const directory = document.getElementById('video_dir').value; const select = document.getElementById('video'); if (!directory) return; select.innerHTML = '<option>Loading...</option>'; const response = await fetch('/api/videos?directory=' + encodeURIComponent(directory)); const data = await response.json(); select.innerHTML = data.videos.length ? data.videos.map(path => '<option value="' + path.replaceAll('&', '&amp;').replaceAll('"', '&quot;') + '">' + path.replaceAll('&', '&amp;').replaceAll('<', '&lt;') + '</option>').join('') : '<option value="">No videos found</option>'; }}
async function loadDirectories() {{ const response = await fetch('/api/directories?root=' + encodeURIComponent({json.dumps(str(MODEL_ROOT))})); const data = await response.json(); const select = document.getElementById('dataset'); select.innerHTML = data.directories.length ? data.directories.map(path => '<option value="' + path.replaceAll('&', '&amp;').replaceAll('"', '&quot;') + '">' + path.replaceAll('&', '&amp;').replaceAll('<', '&lt;') + '</option>').join('') : '<option value="">No directories found</option>'; }}
async function loadMounts() {{ const response = await fetch('/api/mounts'); const data = await response.json(); const select = document.getElementById('mount_root'); select.innerHTML = data.mounts.length ? data.mounts.map(path => '<option value="' + path.replaceAll('&', '&amp;').replaceAll('"', '&quot;') + '">' + path.replaceAll('&', '&amp;').replaceAll('<', '&lt;') + '</option>').join('') : '<option value="">No mounted Drive found</option>'; document.getElementById('mount_status').textContent = data.mounts.length ? 'Mounted and accessible' : 'No accessible Drive mount detected'; }}
document.querySelector('[name=model]').addEventListener('change', updateModel); document.getElementById('video_dir').addEventListener('change', loadVideos); updateModel(); toggleSource(); loadDirectories(); loadMounts();
</script></main></body></html>"""


class Handler(BaseHTTPRequestHandler):
    def send_html(self, body, status=200):
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def do_GET(self):
        if self.path == "/":
            self.send_html(page())
            return
        if self.path.startswith("/jobs/"):
            job_id = self.path.rsplit("/", 1)[-1]
            with JOBS_LOCK:
                job = JOBS.get(job_id)
            if job is None:
                self.send_html(page("Job not found"), 404)
                return
            self.send_html("<pre>" + html.escape(json.dumps(job, indent=2)) + "</pre>")
            return
        if self.path.startswith("/api/videos"):
            directory = unquote(parse_qs(urlparse(self.path).query).get("directory", [""])[0])
            folder = Path(directory).expanduser()
            extensions = {".mp4", ".avi", ".mov", ".mkv", ".webm", ".mpeg", ".mpg"}
            videos = sorted(str(path) for path in folder.iterdir() if path.is_file() and path.suffix.lower() in extensions) if folder.is_dir() else []
            payload = json.dumps({"videos": videos}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        if self.path.startswith("/api/directories"):
            root = Path(unquote(parse_qs(urlparse(self.path).query).get("root", [str(MODEL_ROOT)])[0])).expanduser()
            directories = [str(root)]
            if root.is_dir():
                directories.extend(str(path) for path in sorted(root.rglob("*")) if path.is_dir() and "__pycache__" not in path.parts)
            payload = json.dumps({"directories": directories}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        if self.path == "/api/mounts":
            mounts = []
            for drive in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
                root = Path(f"{drive}:\\")
                if root.is_dir():
                    drive_root = root / "My Drive"
                    mounts.append(str(drive_root if drive_root.is_dir() else root))
            payload = json.dumps({"mounts": mounts}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        self.send_html(page("Not found"), 404)

    def do_POST(self):
        if self.path != "/run":
            self.send_html(page("Not found"), 404)
            return
        length = int(self.headers.get("Content-Length", "0"))
        values = {key: items[0].strip() for key, items in parse_qs(self.rfile.read(length).decode()).items() if items}
        model_key = values.get("model", "")
        model = MODELS.get(model_key)
        if model and model["engine"] == "unsupported":
            self.send_html(page("ChakraNet checkpoint found, but its model architecture/source code is not present in this workspace. It cannot be run safely yet."), 400)
            return
        required = ["weights", "lib_parent", "out"]
        if values.get("source", "dataset") == "dataset":
            required.append("dataset")
        else:
            required.extend(["video_dir", "video"])
        if model is None or any(not values.get(key) for key in required):
            self.send_html(page("Select a model and fill in every required field."), 400)
            return
        job_id = str(len(JOBS) + 1)
        source = values.get("source", "dataset")
        dataset = values.get("dataset", "")
        video = values.get("video", "")
        if model["engine"] == "yolo" and source != "video":
            self.send_html(page("The YOLO models require Video from directory input."), 400)
            return
        if source == "video":
            video_path = Path(video)
            if not video_path.is_file() or video_path.parent.resolve() != Path(values["video_dir"]).resolve():
                self.send_html(page("Choose a video that exists in the selected video directory."), 400)
                return
            dataset = str(Path(tempfile.gettempdir()) / f"polyp_video_job_{job_id}")
            images_dir = Path(dataset) / "data_C1" / "images_C1"
            images_dir.mkdir(parents=True, exist_ok=True)
            import cv2
            capture = cv2.VideoCapture(str(video_path))
            frame_number = 0
            while True:
                success, frame = capture.read()
                if not success:
                    break
                cv2.imwrite(str(images_dir / f"frame_{frame_number:06d}.jpg"), frame)
                frame_number += 1
            capture.release()
            if frame_number == 0:
                self.send_html(page("The selected video did not contain readable frames."), 400)
                return
        if model["engine"] == "yolo":
            output = Path(values["out"]) / f"{Path(video).stem}_{model_key}_annotated.mp4"
            command = [sys.executable, str(ROOT / "video_infer.py"), "--weights", values["weights"], "--source", video, "--output", str(output), "--device", values.get("device", "cuda"), "--threshold", values.get("thresh", "0.5")]
        else:
            command = [sys.executable, str(model["script"]), "--dataset", dataset, "--weights", values["weights"], "--lib_parent", values["lib_parent"], "--out", values["out"], "--thresh", values.get("thresh", "0.5"), "--device", values.get("device", "cuda")]
        if values.get("device"):
            command.extend(["--device", values["device"]])
        with JOBS_LOCK:
            JOBS[job_id] = {"status": "running", "command": command, "output": ""}

        def run():
            process = subprocess.run(command, cwd=ROOT, capture_output=True, text=True)
            with JOBS_LOCK:
                JOBS[job_id] = {"status": "completed" if process.returncode == 0 else "failed", "returncode": process.returncode, "command": command, "output": process.stdout + process.stderr}

        threading.Thread(target=run, daemon=True).start()
        self.send_html(page(job_id=job_id))

    def log_message(self, format, *args):
        print(f"[{self.log_date_time_string()}] {format % args}")


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    print(f"Backend listening on http://0.0.0.0:{PORT}")
    server.serve_forever()