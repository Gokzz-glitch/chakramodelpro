import argparse
from pathlib import Path

import cv2
from ultralytics import YOLO


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", required=True)
    parser.add_argument("--source", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--device", default="cuda")
    parser.add_argument("--threshold", type=float, default=0.5)
    args = parser.parse_args()

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    capture = cv2.VideoCapture(args.source)
    if not capture.isOpened():
        raise SystemExit(f"Unable to open video: {args.source}")
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH)) or 640
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT)) or 480
    fps = capture.get(cv2.CAP_PROP_FPS) or 25.0
    writer = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (width, height))
    model = YOLO(args.weights)
    while True:
        success, frame = capture.read()
        if not success:
            break
        result = model.predict(frame, conf=args.threshold, device=args.device, verbose=False)[0]
        writer.write(result.plot())
    capture.release()
    writer.release()
    print(f"Saved annotated video: {output}")


if __name__ == "__main__":
    main()