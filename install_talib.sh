#!/bin/bash

set -e

echo "✅ 1. Installing build dependencies..."
sudo apt update
sudo apt install -y build-essential wget git python3-dev libffi-dev

echo "✅ 2. Cloning TA-Lib C library from GitHub..."
git clone https://github.com/TA-Lib/ta-lib.git
cd ta-lib

echo "✅ 3. Building and installing TA-Lib C library..."
./configure --prefix=/usr
make -j$(nproc)
sudo make install
cd ..
rm -rf ta-lib

echo "✅ 4. Installing compatible NumPy version (1.24.4)..."
pip uninstall -y numpy || true
pip install numpy==1.24.4

echo "✅ 5. Installing TA-Lib Python binding..."
CFLAGS="-I/usr/include" LDFLAGS="-L/usr/lib" LD_LIBRARY_PATH=/usr/lib pip install --no-cache-dir TA-Lib

echo "🎉 Installation complete! Test it using: python3 -c 'import talib; print(talib.SMA([1,2,3,4,5], timeperiod=2))'"
