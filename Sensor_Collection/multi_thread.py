import threading
import time
from collections import deque

import non_stitch
import log


# ============================
# GLOBAL SHARED STATE
# ============================

START_TIME = time.time()

def now():
    return time.time() - START_TIME


YOLO_BUFFER = deque(maxlen=100)   # ~3 seconds at 30 FPS
FUSION_WINDOW = 0.05               # 50 ms

yolo_ready = threading.Event()
stop_event = threading.Event()


# ============================
# FUSION LOGIC
# ============================

def match_yolo(sensor_time):
    """
    Find the closest YOLO detection within FUSION_WINDOW.
    Returns None if no match found.
    """
    best = None
    best_dt = float("inf")

    for ev in reversed(YOLO_BUFFER):
        dt = abs(sensor_time - ev["time"])
        if dt <= FUSION_WINDOW and dt < best_dt:
            best = ev
            best_dt = dt
        elif ev["time"] < sensor_time - FUSION_WINDOW:
            # Early exit: too old, won't find better matches
            break

    return best


# ============================
# THREAD STARTERS
# ============================

def start_yolo():
    """Run YOLO detection in separate thread"""
    print("[SYSTEM] Starting YOLO thread...")
    try:
        non_stitch.run(
            now=now,
            yolo_buffer=YOLO_BUFFER,
            yolo_ready=yolo_ready,
            stop_event=stop_event
        )
    except Exception as e:
        print(f"[ERROR] YOLO thread crashed: {e}")
        stop_event.set()  # Signal other threads to stop


def start_arduino():
    """Run Arduino sensor logging in separate thread"""
    print("[SYSTEM] Waiting for YOLO to be ready...")
   
   
    print("[SYSTEM] Starting Arduino thread...")
   
    try:
        log.loop(
            now=now,
            match_yolo=match_yolo,
            stop_event=stop_event
        )
    except Exception as e:
        print(f"[ERROR] Arduino thread crashed: {e}")
        stop_event.set()  # Signal other threads to stop


# ============================
# MAIN
# ============================

if __name__ == "__main__":

    t1 = threading.Thread(target=start_yolo, daemon=True)
    t2 = threading.Thread(target=start_arduino, daemon=True)

    t1.start()
    t2.start()

    print("[SYSTEM] Threads running. Press Ctrl+C to exit.")

    try:
        while not stop_event.is_set():
            time.sleep(0.5)  # Check more frequently
    except KeyboardInterrupt:
        print("\n[SYSTEM] Interrupt received, stopping...")
        stop_event.set()

    # Give threads time to clean up gracefully
    print("[SYSTEM] Waiting for threads to finish...")
    t1.join(timeout=5)
    t2.join(timeout=5)

    # Check if threads are still alive
    if t1.is_alive() or t2.is_alive():
        print("[WARNING] Some threads did not stop gracefully")
   
    print("[SYSTEM] Clean shutdown.")
    
    