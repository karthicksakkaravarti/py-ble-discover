from kivy.core.window import Window
import asyncio
import bleak
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window  # Import Window
from kivy.logger import Logger
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
import logging
from kivy.animation import Animation

# Set the logger for Kivy
logging.Logger.manager.root = Logger

Window.size = (700, 670)


class IndeterminateProgressBar(ProgressBar):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.max = 100
        self.value = 0
        self.start_animation()

    def start_animation(self):
        anim = Animation(value=self.max, duration=1) + \
            Animation(value=0, duration=1)
        anim.repeat = True
        anim.start(self)


class BluetoothDeviceItem(BoxLayout):
    """Custom layout for each Bluetooth device in the list."""

    def __init__(self, device, connect_callback, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.device = device
        device_info = f"{device.name} ({device.address})"
        if hasattr(device, 'rssi'):  # Check if RSSI information is available
            device_info += f" - Signal: {device.rssi}dBm"
        self.add_widget(Label(text=device_info, size_hint_x=0.8))
        self.connect_button = Button(text="Connect", size_hint_x=0.2)
        self.connect_button.bind(
            on_press=lambda instance: connect_callback(device))
        self.add_widget(self.connect_button)


class BluetoothScannerApp(App):
    """Main app for scanning and displaying Bluetooth devices."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.running = True
        self.scanned_devices = []
        self.all_discovered_devices = []  # List to store all discovered devices
        self.device_layout = BoxLayout(
            orientation='vertical', spacing=10, size_hint_y=None)
        self.device_layout.bind(
            minimum_height=self.device_layout.setter('height'))

    def show_progress_bar(self):
        self.progress_bar.opacity = 1
        self.progress_bar.disabled = False

    def hide_progress_bar(self):
        self.progress_bar.opacity = 0
        self.progress_bar.disabled = True

    def build(self):
        """Build the UI components."""
        main_layout = BoxLayout(orientation='vertical', spacing=10)

        # Filter and Sorting UI
        control_layout = BoxLayout(
            orientation='horizontal', size_hint_y=0.1, height=50)

        # Filter Spinner
        self.filter_spinner = Spinner(
            text='Filter',
            values=('All Devices', 'Paired Devices', 'Unpaired Devices'),
            size_hint_x=0.5
        )
        self.filter_spinner.bind(text=self.on_filter_select)
        control_layout.add_widget(self.filter_spinner)

        # Sorting Spinner
        self.sort_spinner = Spinner(
            text='Sort by',
            values=('Name', 'Signal Strength'),
            size_hint_x=0.5
        )
        self.sort_spinner.bind(text=self.on_sort_select)
        control_layout.add_widget(self.sort_spinner)

        main_layout.add_widget(control_layout)

        # ProgressBar for scanning indication
        # Add IndeterminateProgressBar
        self.progress_bar = IndeterminateProgressBar(
            size_hint_y=None, height=20)
        main_layout.add_widget(self.progress_bar)

        # Search Input
        self.search_input = TextInput(
            size_hint_y=None,
            height=44,
            hint_text='Search for devices'
        )
        self.search_input.bind(text=self.on_search_text)
        main_layout.add_widget(self.search_input)

        scroll_view = ScrollView(size_hint=(
            1, None), size=(Window.width, Window.height))
        scroll_view.add_widget(self.device_layout)
        main_layout.add_widget(scroll_view)

        return main_layout

    def on_search_text(self, instance, value):
        """Filter the list of devices based on the search query."""
        if not value:
            # If the search query is empty, show all devices
            filtered_devices = self.scanned_devices
        else:
            # Filter devices based on the query (name or address)
            filtered_devices = [d for d in self.scanned_devices if value.lower(
            ) in d.name.lower() or value.lower() in d.address.lower()]

        self.update_device_list(filtered_devices)

    def on_filter_select(self, spinner, text):
        if text == 'Paired Devices':
            filtered_devices = [d for d in self.scanned_devices if d.is_paired]
        elif text == 'Unpaired Devices':
            filtered_devices = [
                d for d in self.scanned_devices if not d.is_paired]
        else:
            filtered_devices = self.scanned_devices
        self.update_device_list(filtered_devices)

    def on_sort_select(self, spinner, text):
        # Implement the logic for sorting devices
        if text == 'Name':
            sorted_devices = sorted(self.scanned_devices, key=lambda d: d.name)
        elif text == 'Signal Strength':
            sorted_devices = sorted(
                self.scanned_devices, key=lambda d: d.rssi, reverse=True)
        else:
            sorted_devices = self.scanned_devices
        self.update_device_list(sorted_devices)

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
                self.show_progress_bar()  # Show the progress bar
                Logger.info("BluetoothScanner: Scanning for devices...")
                scanned_devices = await bleak.BleakScanner.discover(1)
                Logger.info("BluetoothScanner: Scan complete")
                for device in scanned_devices:
                    if device not in self.all_discovered_devices:
                        self.all_discovered_devices.append(device)
                self.update_device_list(self.all_discovered_devices)
                await asyncio.sleep(5)  # Add delay for periodic scanning
            except bleak.exc.BleakError as e:
                Logger.error(f"BluetoothScanner: Error - {e}")
            finally:
                self.hide_progress_bar()  # Hide the progress bars

    async def connect_to_device(self, device):
        """Attempt to connect to the selected Bluetooth device."""
        Logger.info(
            f"BluetoothScanner: Attempting to connect to {device.name}")
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
