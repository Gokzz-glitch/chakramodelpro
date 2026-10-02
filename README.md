# ChakraNet Polyp Evaluation Project

This project provides a small browser interface for running polyp-detection and polyp-segmentation models on local videos or image datasets.

The project is designed for a beginner: choose a model, choose the input type, select a directory or video, set a confidence threshold, and start an evaluation job.

## Important Note About Model Weights

Model weights are intentionally excluded from GitHub because they are large binary files. They remain on the local Drive and must be copied into the matching model folder after downloading this project.

Ignored weight/archive extensions are:

- `.pth`
- `.pt`
- `.zip`

The source packages supplied with this project therefore contain code, manifests, documentation, and the ChakraNet architecture notebook, but not the model weights.

## What The Project Does

1. Starts a local Python web backend.
2. Shows a browser form at `http://127.0.0.1:8000`.
3. Lets you choose one of six model entries.
4. Detects mounted Windows Google Drive roots.
5. Lists directories and videos available to the backend.
6. Runs video inference for Ultralytics YOLO models.
7. Runs the existing PraNet/PVT dataset evaluators when their library source is available.
8. Saves annotated videos or evaluation reports to the selected output directory.

## Six Model Entries

### 1. PraNet-V1

A segmentation model using a Res2Net50-style backbone. It expects:

- `models/pranet_v1/weights.pth`
- the model repository `lib` source package
- the PraNet evaluator script

The supplied `RES-V1.pth` checkpoint is not committed to GitHub.

### 2. PVT-PraNet-V1

A segmentation model using a PVTv2-B2 backbone. It expects:

- `models/pvt_pranet_v1/weights.pth`
- the model repository `lib` source package
- the PVT evaluator script
- the PVTv2-B2 backbone file required by the original model code

The supplied `PVT-V1.pth` checkpoint is not committed to GitHub.

### 3. Root YOLO

Ultralytics YOLO checkpoint copied from the root `yolo_best.pt` file. It is used by `video_infer.py`.

### 4. YOLOViT VIT

Ultralytics-compatible checkpoint copied from `yolovit/VIT.pt`.

### 5. YOLOViT YOLO

Ultralytics-compatible checkpoint copied from `yolovit/yolo_best.pt`.

### 6. AdaBN-ChakraNet

The ChakraNet checkpoint and the original architecture notebook are stored locally. The notebook describes an AdaBN-ChakraNet based on a PraNet ResNet-101 design.

The notebook is included as `models/chakranet/architecture_source.ipynb`, but the browser backend does not yet run this notebook directly as a live inference worker.

## Directory Tree

```text
valid models/
|-- README.md
|-- .gitignore
|-- backend.py
|-- video_infer.py
|-- PraNetV1-res2Net/
|   |-- evaluate_pranetv1_polypgen_full.py
|   `-- Pranet-res2Net_summary.md
|-- PVT-PRaNet-v1/
|   |-- evaluate_pvt_pranetv1_polypgen_full.py
|   `-- PVT-Pranet summary.md
|-- yolovit/
|   |-- VIT.pt                 [local only, ignored by Git]
|   `-- yolo_best.pt           [local only, ignored by Git]
|-- models/
|   |-- pranet_v1/
|   |   |-- model.json
|   |   |-- weights.pth         [local only, ignored by Git]
|   |   `-- evaluate_pranetv1_polypgen_full.py
|   |-- pvt_pranet_v1/
|   |   |-- model.json
|   |   |-- weights.pth         [local only, ignored by Git]
|   |   `-- evaluate_pvt_pranetv1_polypgen_full.py
|   |-- yolo_root/
|   |   |-- model.json
|   |   `-- weights.pt           [local only, ignored by Git]
|   |-- yolovit_vit/
|   |   |-- model.json
|   |   `-- weights.pt           [local only, ignored by Git]
|   |-- yolovit_yolo/
|   |   |-- model.json
|   |   `-- weights.pt           [local only, ignored by Git]
|   `-- chakranet/
|       |-- model.json
|       |-- architecture_source.ipynb
|       |-- weights.pth           [local only, ignored by Git]
|       `-- student_teacher.zip   [local only, ignored by Git]
`-- model_packages/
    |-- pranet_v1_source.zip
    |-- pvt_pranet_v1_source.zip
    |-- yolo_root_source.zip
    |-- yolovit_vit_source.zip
    |-- yolovit_yolo_source.zip
    |-- chakranet_source.zip
    `-- all_model_sources.zip
```

## How To Start The Backend

Open PowerShell in the project directory:

```powershell
cd "J:\My Drive\valid models"
python backend.py
```

Then open:

```text
http://127.0.0.1:8000
```

Keep the PowerShell window running while using the browser interface.

## How To Use The Browser Form

1. Select a model.
2. Select `Dataset directory` for an image dataset or `Video from directory` for a video.
3. Choose a mounted Google Drive root if needed.
4. Choose the input directory or video.
5. Confirm the automatically filled checkpoint and library paths.
6. Select `CUDA GPU` when PyTorch and CUDA are working.
7. Change the threshold. A higher value produces fewer detections; a lower value produces more detections.
8. Choose an output directory.
9. Press `Start evaluation`.
10. Open the job status link to inspect the command and output.

## Video Processing

`video_infer.py` loads an Ultralytics model, reads the input video frame by frame, draws model predictions, and writes an annotated MP4 file to the output directory.

Example:

```powershell
python video_infer.py `
  --weights "models\yolo_root\weights.pt" `
  --source "I:\My Drive\colon cancer\colon_cancer_dataset\videos with polyps\1_1.avi" `
  --output "I:\My Drive\colon cancer\outputs\1_1_annotated.mp4" `
  --device cuda `
  --threshold 0.5
```

## Dataset Evaluation

The PraNet and PVT scripts discover PolypGen-style folders such as:

```text
data_C1/images_C1/
data_C1/masks_C1/
sequenceData/positive/seq1/
sequenceData/negativeOnly/seq1_neg/
```

They create reviewed images, CSV/Excel indexes, and a Markdown summary.

## Python Packages

The YOLO video path requires:

```powershell
pip install ultralytics opencv-python
```

The segmentation evaluators additionally require the dependencies used by their original repositories, including PyTorch, OpenCV, NumPy, and usually `openpyxl`.

For GPU use, install a PyTorch build compatible with the installed NVIDIA driver and CUDA runtime. Verify it with:

```powershell
python -c "import torch; print(torch.cuda.is_available()); print(torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU only')"
```

## Troubleshooting

### The browser does not open

Confirm that `python backend.py` is still running and use `http://127.0.0.1:8000`.

### A model path is empty or invalid

The checkpoint is not included in GitHub. Copy the local checkpoint into the matching `models/<model_name>/` folder and name it `weights.pth` or `weights.pt` as shown in the tree.

### PraNet or PVT reports a missing `lib` directory

The checkpoint alone is not enough. The original model source package must be placed inside the model folder or its configured library parent. The evaluator expects a real `lib` package containing the model implementation and backbone modules.

### CUDA fails

This is an environment problem, not a threshold problem. Check the PyTorch installation, NVIDIA driver, CUDA compatibility, and the selected Python interpreter.

### ChakraNet does not start

The notebook is architecture documentation and source, not a standalone command-line inference application. A runner must be extracted from the notebook before it can be connected to the live backend.

## GitHub Repository

The non-weight project source is published at:

https://github.com/Gokzz-glitch/chakramodelpro

Large checkpoints remain local by design.
