import time
import serial
import os

port = 'COM3'
baud = 115200
sensor_ser = None
first_read = True 

# ============================
# LOG FILE SETUP
# ============================

script_dir = os.path.dirname(os.path.abspath(__file__))
log_dir = os.path.join(script_dir, "logs")
os.makedirs(log_dir, exist_ok=True)

start_time_str = time.strftime("%m.%d.%y-%H.%M")
log_file = os.path.join(log_dir, f"{start_time_str}.log")

# ============================
# MAIN LOOP (THREADED MODE)
# ============================

def loop(now, match_yolo, stop_event):
    """Main loop for threaded execution"""
    global sensor_ser

    print("[LOGGER] loop() entered")
    serial_init()

    print(f"[LOGGER] Logging to: {os.path.abspath(log_file)}")

    with open(log_file, "a") as f:
        f.write("=== LOGGER STARTED ===\n")
        f.flush()

    last_heartbeat = time.time()

    while not stop_event.is_set():
        read_sensor(now, match_yolo)

        if time.time() - last_heartbeat >= 1.0:
           
            last_heartbeat = time.time()

        time.sleep(0.2)

    if sensor_ser is not None:
        try:
            sensor_ser.close()
            print("[LOGGER] Serial port closed")
        except:
            pass

# ============================
# SERIAL INIT
# ============================

def serial_init():
    global sensor_ser
    try:
        sensor_ser = serial.Serial(port, baud, timeout=1)
        print(f"[LOGGER] Connected to Arduino on {port}")
    except serial.SerialException as e:
        print(f"[LOGGER] FAILED to connect on {port}: {e}")
        sensor_ser = None

# ============================
# SENSOR READ
# ============================

def read_sensor(now, match_yolo):
    global sensor_ser, first_read

    if sensor_ser is None:
        serial_init()
        if sensor_ser is None:
            return

    try:
        line = sensor_ser.readline().decode("utf-8").strip()
        if not line:
            return
    except serial.SerialException as e:
        print(f"[LOGGER] Serial error: {e}")
        sensor_ser = None
        return

    if first_read:
        print("[LOGGER] FIRST SENSOR DATA RECEIVED")
        first_read = False

    print(f"[LOGGER] Received: {line}")

    sensor_time = now()
    yolo_match = match_yolo(sensor_time)

    log_event(line, sensor_time, yolo_match)

# ============================
# FILE LOGGING
# ============================

def log_event(line, sensor_time, yolo_match=None):
    timestamp = time.strftime("[%Y-%m-%d %H:%M:%S]")

    try:
        with open(log_file, "a") as f:
            if yolo_match:
                log_line = f"{timestamp} {line} | YOLO: {yolo_match}\n"
            else:
                log_line = f"{timestamp} {line}\n"

            f.write(log_line)
            f.flush()

        print(f"[LOGGER] Logged")

    except Exception as e:
        print(f"[LOGGER] LOGGING ERROR: {e}")

# ============================
# STANDALONE MODE
# ============================

def main():
    print("[LOGGER] running in STANDALONE mode")
    serial_init()
    print(f"[LOGGER] Logging to: {os.path.abspath(log_file)}")

    with open(log_file, "a") as f:
        f.write("=== LOGGER STARTED (STANDALONE) ===\n")
        f.flush()

    try:
        while True:
            read_sensor(lambda: time.time(), lambda t: None)
            time.sleep(0.2)
    except KeyboardInterrupt:
        print("[LOGGER] exiting")
        if sensor_ser is not None:
            sensor_ser.close()

# ============================
if __name__ == "__main__":
    main()
