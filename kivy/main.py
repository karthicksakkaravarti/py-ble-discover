import asyncio
import bleak
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window  # Import Window
from kivy.logger import Logger
import logging

# Set the logger for Kivy
logging.Logger.manager.root = Logger

class BluetoothDeviceItem(BoxLayout):
    """Custom layout for each Bluetooth device in the list."""
    def __init__(self, device, connect_callback, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.device = device
        self.add_widget(Label(text=f"{device.name} ({device.address})", size_hint_x=0.8))
        self.connect_button = Button(text="Connect", size_hint_x=0.2)
        self.connect_button.bind(on_press=lambda instance: connect_callback(device))
        self.add_widget(self.connect_button)

class BluetoothScannerApp(App):
    """Main app for scanning and displaying Bluetooth devices."""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = True
        self.device_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.device_layout.bind(minimum_height=self.device_layout.setter('height'))

    def build(self):
        """Build the UI components."""
        scroll_view = ScrollView(size_hint=(1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(self.device_layout)
        return scroll_view

    def update_device_list(self, devices):
        """Update the list of devices displayed."""
        self.device_layout.clear_widgets()
        for device in devices:
            item = BluetoothDeviceItem(device, self.connect_to_device)
            self.device_layout.add_widget(item)

    async def scan_and_display_devices(self):
        """Scan for Bluetooth devices and update the display."""
        while self.running:
            try:
                Logger.info("BluetoothScanner: Scanning for devices...")
                scanned_devices = await bleak.BleakScanner.discover(1)
                Logger.info("BluetoothScanner: Scan complete")
                self.update_device_list(scanned_devices)
                await asyncio.sleep(5)  # Add delay for periodic scanning
            except bleak.exc.BleakError as e:
                Logger.error(f"BluetoothScanner: Error - {e}")

    async def connect_to_device(self, device):
        """Attempt to connect to the selected Bluetooth device."""
        Logger.info(f"BluetoothScanner: Attempting to connect to {device.name}")
        try:
            async with bleak.BleakClient(device) as client:
                # Handle successful connection here
                Logger.info(f"BluetoothScanner: Connected to {device.name}")
        except bleak.exc.BleakError as e:
            Logger.error(f"BluetoothScanner: Connection error - {e}")

    def on_stop(self):
        """Handle stopping the app."""
        self.running = False

async def main(app):
    """Entry point for running the app with asyncio."""
    await asyncio.gather(app.async_run("asyncio"), app.scan_and_display_devices())

if __name__ == "__main__":
    Logger.setLevel(logging.DEBUG)
    app = BluetoothScannerApp()
    asyncio.run(main(app))
