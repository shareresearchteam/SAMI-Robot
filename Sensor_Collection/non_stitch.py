import cv2  # type: ignore
import csv
import os
from datetime import datetime
from ultralytics import YOLO  # type: ignore
import numpy as np
import torch
import time


def run(now, yolo_buffer, yolo_ready, stop_event):

    # =============================
    # Configuration
    # =============================
    MODEL_PATH = "yolov8n.pt"
    CONF_THRESHOLD = 0.7
    CAMERA_INDICES = [0, 1]
    OUTPUT_DIR = "../videos_outputs"
    OUTPUT_CSV = "multi_camera_detections.csv"

    FRAME_WIDTH = 640
    FRAME_HEIGHT = 480
    FPS = 30
    IMG_SIZE = 224

    DRAW = True          # Turn off to gain speed
    CSV_BUFFER_SIZE = 30 # Write CSV every N frames

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # =============================
    # Load YOLO model
    # =============================
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Using device: {device}")

    model = YOLO(MODEL_PATH)
    model.to(device)

    # =============================
    # Initialize cameras & writers
    # =============================
    caps = []
    writers = []

    for cam_index in CAMERA_INDICES:
        cap = cv2.VideoCapture(cam_index)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open camera {cam_index}")

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, FRAME_WIDTH)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, FRAME_HEIGHT)
        cap.set(cv2.CAP_PROP_FPS, FPS)

        caps.append(cap)

        video_path = os.path.join(OUTPUT_DIR, f"camera_{cam_index}.avi")
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        writer = cv2.VideoWriter(video_path, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))
        writers.append(writer)

        print(f"Camera {cam_index} initialized → {video_path}")

    # =============================
    # CSV setup
    # =============================
    csv_file = open(OUTPUT_CSV, "w", newline="")
    csv_writer = csv.writer(csv_file)

    header = ["Timestamp", "SystemTime"]
    for i in range(len(CAMERA_INDICES)):
        header += [f"Cam{i}_Count", f"Cam{i}_Detection", f"Cam{i}_BoxAreas"]
    header.append("Total_Count")
    #csv_writer.writerow(header)

    csv_buffer = []

    print("=" * 60)
    print("Running OPTIMIZED multi-camera YOLO (batched)")
    print("=" * 60)

    print("[YOLO] Initialization complete — ready")
    yolo_ready.set()
    try:
        while not stop_event.is_set():
            loop_start = time.time()

            frames = []
            frame_map = []  # maps batch index → camera index

            # -----------------------------
            # Capture frames
            # -----------------------------
            for cam_idx, cap in enumerate(caps):
                ret, frame = cap.read()
                if ret:
                    frames.append(frame)
                    frame_map.append(cam_idx)

            # Initialize outputs
            per_camera_counts = [0] * len(caps)
            per_camera_detection = [False] * len(caps)
            per_camera_box_areas = [[] for _ in range(len(caps))]

            # -----------------------------
            # YOLO batch inference
            # -----------------------------
            if frames:
                with torch.no_grad():
                    results = model(frames, imgsz=IMG_SIZE, verbose=False)

                for batch_idx, (res, cam_idx) in enumerate(zip(results, frame_map)):
                    boxes = res.boxes
                    if boxes is None or len(boxes) == 0:
                        continue

                    cls = boxes.cls.cpu().numpy()
                    conf = boxes.conf.cpu().numpy()
                    xyxy = boxes.xyxy.cpu().numpy()

                    mask = (cls == 0) & (conf >= CONF_THRESHOLD)
                    count = int(mask.sum())

                    per_camera_counts[cam_idx] = count
                    per_camera_detection[cam_idx] = count > 0

                    # Calculate box areas for detected persons
                    box_areas = []
                    for (x1, y1, x2, y2) in xyxy[mask]:
                        width = x2 - x1
                        height = y2 - y1
                        area = width * height
                        box_areas.append(int(area))
                    
                    per_camera_box_areas[cam_idx] = box_areas

                    if DRAW and count > 0:
                        annotated = frames[batch_idx]

                        for (x1, y1, x2, y2), c in zip(xyxy[mask], conf[mask]):
                            cv2.rectangle(
                                annotated,
                                (int(x1), int(y1)),
                                (int(x2), int(y2)),
                                (0, 255, 0),
                                2,
                            )

            # -----------------------------
            # Display, save, log
            # -----------------------------
            timestamp = now()
            total_people = sum(per_camera_counts)
            yolo_event = {
                "time": timestamp,
                "total": total_people,
                "per_camera": per_camera_counts
            }
            
            if timestamp < 2.0:
                continue
            
            yolo_buffer.append(yolo_event)

            # Iterate over captured frames
            for batch_idx, cam_idx in enumerate(frame_map):
                frame = frames[batch_idx]
                if DRAW:
                    cv2.putText(
                        frame,
                        f"{timestamp:.3f}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (255, 255, 255),
                        2,
                    )
                    cv2.imshow(f"Camera {CAMERA_INDICES[cam_idx]}", frame)

                writers[cam_idx].write(frame)

            row = [timestamp, time.time()]
            for count, detected, box_areas in zip(per_camera_counts, per_camera_detection, per_camera_box_areas):
                # Convert box_areas list to string format
                areas_str = ";".join(map(str, box_areas)) if box_areas else ""
                row += [count, detected, areas_str]
            row.append(total_people)
            
            csv_buffer.append(row)

            if len(csv_buffer) >= CSV_BUFFER_SIZE:
                #csv_writer.writerows(csv_buffer)
                csv_buffer.clear()

            # -----------------------------
            # Exit
            # -----------------------------
            if cv2.waitKey(1) & 0xFF == ord("q"):
                print("Q pressed → Exiting...")
                stop_event.set()
                break

          

    finally:
        print("Cleaning up...")

        for cap in caps:
            cap.release()
        for w in writers:
            w.release()

        if csv_buffer:
            csv_writer.writerows(csv_buffer)

        csv_file.close()
        cv2.destroyAllWindows()

        print("Videos saved in:", OUTPUT_DIR)


if __name__ == "__main__":
    run()