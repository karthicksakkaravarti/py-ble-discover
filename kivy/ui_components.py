from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.animation import Animation
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle


class BluetoothDeviceItem(BoxLayout):
    def __init__(self, device, connect_callback, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.size_hint_y = None  # Allow height to be set manually
        self.device = device
        self.height = dp(50)  # Example: Set height to 50dp
        device_info = f"{device.name} ({device.address})"
        if hasattr(device, 'rssi'):  # Check if RSSI information is available
            device_info += f" - Signal: {device.rssi}dBm"
        self.add_widget(Label(text=device_info, size_hint_x=0.8))
        self.connect_button = Button(text="Connect", size_hint_x=0.2)
        self.connect_button.bind(
            on_press=lambda instance: connect_callback(device))
        self.add_widget(self.connect_button)


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


class CustomButton(Button):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (None, None)
        self.size = (dp(100), dp(40))
        self.pos_hint = {'right': 1, 'top': 1}
        with self.canvas.before:
            Color(0.1, 0.5, 0.8, 0.9)  # RGBA Color
            self.rect = RoundedRectangle(size=self.size, radius=[10])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

class ScanningDeviceItem(BoxLayout):
    def __init__(self, device, **kwargs):
        super().__init__(orientation='horizontal', **kwargs)
        self.size_hint_y = None
        self.height = dp(50)
        device_info = f"{device.name} ({device.address})"
        if hasattr(device, 'rssi'):
            device_info += f" - Signal: {device.rssi}dBm"
        self.add_widget(Label(text=device_info, size_hint_x=0.8))