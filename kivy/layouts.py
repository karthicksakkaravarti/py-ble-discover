from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from ui_components import IndeterminateProgressBar, BluetoothDeviceItem
from utils import Window, on_filter_select, on_sort_select, hide_progress_bar
from kivy.uix.label import Label


def build_main_layout(app_instance):
    main_layout = BoxLayout(orientation='vertical', spacing=10)
    # Add a button to toggle scanning
    app_instance.scan_button = Button(text="Start Scanning",
                                      size_hint_y=None, height=44)
    app_instance.scan_button.bind(on_press=app_instance.toggle_scanning)
    main_layout.add_widget(app_instance.scan_button)

    # ProgressBar for scanning indication
    # Add IndeterminateProgressBar
    app_instance.progress_bar = IndeterminateProgressBar(
        size_hint_y=None, height=20)
    main_layout.add_widget(app_instance.progress_bar)

    hide_progress_bar(app_instance)

    # Horizontal layout for top elements
    top_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)

    # Label for device count
    app_instance.device_count_label = Label(
        text="Devices Found: 0",
        size_hint_x=None,
        width=400
    )
    top_layout.add_widget(app_instance.device_count_label)

    # Save Button
    save_button = Button(
        text='Save Devices',
        size_hint_x=None,
        width=300
    )
    save_button.bind(on_press=lambda x: app_instance.save_device_list())
    top_layout.add_widget(save_button)

    # Search Element
    app_instance.search_input = TextInput(
        hint_text='Search for devices',
        size_hint_x=None,
        width=600,
        tab_width=20
    )
    app_instance.search_input.bind(text=app_instance.on_search_text)
    top_layout.add_widget(app_instance.search_input)

    # Add the top layout to the main layout
    main_layout.add_widget(top_layout)

    app_instance.device_layout = BoxLayout(
            orientation='vertical', spacing=10, size_hint_y=None)
    app_instance.device_layout.bind(
        minimum_height=app_instance.device_layout.setter('height'))

    scroll_view = ScrollView(size_hint=(
            1, None), size=(Window.width, Window.height))
    scroll_view.add_widget(app_instance.device_layout)
    main_layout.add_widget(scroll_view)

    # Add components to main_layout
    return main_layout
