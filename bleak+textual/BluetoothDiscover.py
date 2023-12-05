import asyncio
from textual.app import App
from textual.widgets import Header, Footer, Button, ScrollView, TreeControl
from textual.reactive import Reactive
from bleak import discover

class BluetoothScannerApp(App):
    devices = Reactive([])

    async def on_mount(self):
        # Dock the header and footer
        await self.view.dock(Header(), edge='top')
        await self.view.dock(Footer(), edge='bottom')

        # Device list in a scroll view
        self.device_list = TreeControl("Discovered Devices", {})
        await self.view.dock(ScrollView(self.device_list), edge='left', size=40)

        # Trigger device discovery
        asyncio.create_task(self.discover_devices())

    async def discover_devices(self):
        while True:
            discovered_devices = await discover()
            self.update_device_list(discovered_devices)
            await asyncio.sleep(5)  # Sleep then repeat discovery

    def update_device_list(self, devices):
        # Update the list with the discovered devices
        self.device_list.root.children.clear()
        for device in devices:
            device_name = device.name if device.name else 'Unknown Device'
            self.device_list.root.add(f"{device_name} - {device.address}")

if __name__ == "__main__":
    app = BluetoothScannerApp()
    app.run()
