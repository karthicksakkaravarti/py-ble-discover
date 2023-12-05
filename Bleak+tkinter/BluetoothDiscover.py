import tkinter as tk
from tkinter import ttk
from bleak import discover
import asyncio
import threading

class BluetoothScannerApp:
    def __init__(self, root):
        # Set up the styling for the buttons
        style = ttk.Style()
        style.configure('TButton', font=('Helvetica', 12), borderwidth='4')
        style.theme_use('clam')
        style.configure('TButton', background='#333333', foreground='white')
        style.map('TButton', background=[('active', '#0078D7')])

        self.root = root
        self.root.title("Bluetooth Scanner")
        self.root.configure(bg='#333333')

        # Add a label
        lbl_title = tk.Label(self.root, text="Bluetooth Devices", font=("Helvetica", 24), bg='#333333', fg='white')
        lbl_title.pack(pady=20)

        # Add a frame for listbox and scrollbar
        frame = tk.Frame(self.root, bg='#333333')
        frame.pack(pady=20, fill='both', expand=True)

        # Create a listbox to display devices
        self.listbox_devices = tk.Listbox(frame, width=50, height=10, bg='#333333', fg='white', highlightthickness=0, selectbackground='#555555', activestyle="none")
        self.listbox_devices.pack(side='left', fill='both', expand=True)

        # Create a scrollbar for the listbox
        scrollbar = tk.Scrollbar(frame, orient='vertical', command=self.listbox_devices.yview)
        scrollbar.pack(side='right', fill='y')
        self.listbox_devices.config(yscrollcommand=scrollbar.set)

        # Add Scan and Stop buttons
        btn_scan = ttk.Button(self.root, text="Scan", style='TButton', command=self.start_discovery)
        btn_scan.pack(pady=(20, 10), padx=20, fill='x')

        btn_stop = ttk.Button(self.root, text="Stop", style='TButton', command=self.stop_discovery)
        btn_stop.pack(pady=(0, 20), padx=20, fill='x')

        self.devices = []
        self.discovery_running = False

        # Create an asyncio event loop
        self.loop = asyncio.get_event_loop()

    async def discover_devices(self):
        self.devices = await discover()
        self.refresh_device_list()

    def refresh_device_list(self):
        self.listbox_devices.delete(0, tk.END)
        for device in self.devices:
            print(device.metadata)
            # If the device name is None, display 'Unknown Device' or similar
            device_name = device.name if device.name else 'Unknown Device'
            # Display the first service UUID if available, otherwise display 'Unknown Type'
            device_type = device.metadata['uuids'][0] if device.metadata.get('uuids') else 'Unknown Type'
            device_info = f"{device_name} - {device.address} - {device_type}"
            self.listbox_devices.insert(tk.END, device_info)

    def start_discovery(self):
        if not self.discovery_running:
            self.discovery_running = True
            self.schedule_discovery()

    def schedule_discovery(self):
        if self.discovery_running:
            # Schedule the next discovery
            self.loop.call_soon_threadsafe(
                asyncio.create_task, self.discover_devices())
            # Call this method again after some time
            self.root.after(5000, self.schedule_discovery)

    def stop_discovery(self):
        self.discovery_running = False

    def on_closing(self):
        # Call this method to close the asyncio loop when the application exits
        self.loop.call_soon_threadsafe(self.loop.stop)
        self.root.destroy()
        asyncio_thread.join()

# Setup and run the application
root = tk.Tk()
app = BluetoothScannerApp(root)

# Run the asyncio event loop in a separate thread
asyncio_thread = threading.Thread(target=app.loop.run_forever, daemon=True)
asyncio_thread.start()

# Bind the window close ('X' button) event to properly close the application
root.protocol("WM_DELETE_WINDOW", app.on_closing)

root.mainloop()
