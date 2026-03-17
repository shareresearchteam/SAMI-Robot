import re
import csv
import ast

LOG_FILE = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\logs\01.23.26-11.33.log"
LOG_FILE = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\logs\02.13.26-11.56.log"

CSV_FILE = r"C:\Users\nguyphu2\Downloads\CAPSTONE\data\clean4\sensor_yolo_clean_filled.csv"

MAX_GAP_SECONDS = 0.5
MAX_GAP_MS = int(MAX_GAP_SECONDS * 1000)

pattern = re.compile(
    r"\[(?P<timestamp>.*?)\]\s*"
    r"(?P<data>[\d\.,\s]+)\s*\|\s*YOLO:\s*(?P<yolo>\{.*\})"
)

rows = []

# -------------------------
# 1. Parse log
# -------------------------
with open(LOG_FILE, "r") as f:
    for line in f:
        match = pattern.search(line)
        if not match:
            continue

        timestamp = match.group("timestamp")
        sensor_values = [v.strip() for v in match.group("data").split(",")]

        if len(sensor_values) != 7:
            continue

        (
            sensor_time_ms,
            pir_left,
            pir_right,
            us_left,
            us_middle,
            us_right,
            unknown_flag
        ) = sensor_values

        yolo = ast.literal_eval(match.group("yolo"))

        rows.append({
            "time": timestamp,
            "sensor_time_ms": int(sensor_time_ms),
            "pir_left": int(pir_left),
            "pir_right": int(pir_right),
            "us_left": float(us_left),
            "us_middle": float(us_middle),
            "us_right": float(us_right),
            "unknown_flag": int(unknown_flag),
            "yolo_total": int(yolo["total"]),
            "yolo_cam0": int(yolo["per_camera"][0]),
            "yolo_cam1": int(yolo["per_camera"][1]),
        })

# -------------------------
# 2. Sort by time
# -------------------------
rows.sort(key=lambda r: r["sensor_time_ms"])

# -------------------------
# 3. Fill YOLO flicker gaps
# -------------------------
for i in range(1, len(rows) - 1):
    prev_row = rows[i - 1]
    curr_row = rows[i]
    next_row = rows[i + 1]

    if (
        prev_row["yolo_total"] > 0 and
        curr_row["yolo_total"] == 0 and
        next_row["yolo_total"] > 0
    ):
        gap_ms = next_row["sensor_time_ms"] - prev_row["sensor_time_ms"]

        if gap_ms <= MAX_GAP_MS:
            curr_row["yolo_total"] = 1
            curr_row["yolo_cam0"] = max(
                prev_row["yolo_cam0"], next_row["yolo_cam0"]
            )
            curr_row["yolo_cam1"] = max(
                prev_row["yolo_cam1"], next_row["yolo_cam1"]
            )

# -------------------------
# 4. Write CSV
# -------------------------
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "time",
        "sensor_time_ms",
        "pir_left",
        "pir_right",
        "us_left",
        "us_middle",
        "us_right",
        "unknown_flag",
        "yolo_total",
        "yolo_cam0",
        "yolo_cam1",
    ])

    for r in rows:
        writer.writerow([
            r["time"],
            r["sensor_time_ms"],
            r["pir_left"],
            r["pir_right"],
            r["us_left"],
            r["us_middle"],
            r["us_right"],
            r["unknown_flag"],
            r["yolo_total"],
            r["yolo_cam0"],
            r["yolo_cam1"],
        ])

