import asyncio
from bluetooth_scanner import BluetoothScannerApp
from utils import setup_logging


def main():
    """Main"""
    setup_logging()
    app = BluetoothScannerApp()
    asyncio.run(app.run_async())


if __name__ == "__main__":
    main()
