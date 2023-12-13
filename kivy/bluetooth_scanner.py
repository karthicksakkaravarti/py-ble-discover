import asyncio
import bleak
from kivy.app import App
from layouts import build_main_layout
from utils import Logger, update_device_list, connect_to_device, hide_progress_bar, show_progress_bar
from kivy.core.window import Window
import csv
from os.path import expanduser

Window.size = (700, 670)


class BluetoothScannerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = True
        self.is_scanning = False  # New attribute to control scanning
        self.all_discovered_devices = []
        self.is_scanning = False
        self.current_search_text = ""  # New attribute to store the search text

    async def run_async(self):
        await asyncio.gather(self.async_run("asyncio"), self.scan_and_display_devices())

    def build(self):
        return build_main_layout(self)

    async def scan_and_display_devices(self):
        seen_devices = {}  # Dictionary to keep track of unique devices
        while self.is_scanning:
            try:
                Logger.info("Scanning for devices...")
                scanned_devices = await bleak.BleakScanner.discover(1)
                Logger.info("Scan complete")
                for device in scanned_devices:
                    if device.name not in seen_devices:
                        seen_devices[device.name] = device
                        self.all_discovered_devices.append(device)
                device_count = len(seen_devices)
                self.device_count_label.text = f"Devices Found: {device_count}"
                if not self.current_search_text:
                    update_device_list(self, list(seen_devices.values()))
                await asyncio.sleep(5)
            except bleak.exc.BleakError as e:
                Logger.error(f"Error - {e}")

    def toggle_scanning(self, instance):
        """Toggle the scanning process."""
        show_progress_bar(self)
        self.is_scanning = not self.is_scanning
        self.scan_button.text = "Stop Scanning" if self.is_scanning else "Start Scanning"
        if self.is_scanning:
            asyncio.create_task(self.scan_and_display_devices())
        else:
            hide_progress_bar(self)

    def on_search_text(self, instance, value):
        self.current_search_text = value
        """Filter the list of devices based on the search query."""
        if not value:
            # If the search query is empty, show all devices
            self.current_search_text = None
            filtered_devices = self.all_discovered_devices

        else:
            # Filter devices based on the query (name or address)
            filtered_devices = [d for d in self.all_discovered_devices if d.name and value.lower(
            ) in d.name.lower() or value.lower() in d.address.lower()]
        update_device_list(self, filtered_devices)

    def save_device_list(self):
        home = expanduser("~")
        file_path = f"{home}/device_list.csv"
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Address'])  # Header
            for device in self.all_discovered_devices:
                writer.writerow([device.name, device.address])
        Logger.info(f"Device list saved to {file_path}")

    def on_stop(self):
        self.running = False
