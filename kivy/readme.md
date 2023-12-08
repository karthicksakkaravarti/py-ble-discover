
# Bluetooth Scanner App

## Introduction
The Bluetooth Scanner App is a desktop application developed using the Kivy framework and Bleak for Bluetooth operations. It's designed to scan for nearby Bluetooth devices, display their details, and allow users to connect to them. The app is suitable for those who need to manage Bluetooth connections and monitor device information in a user-friendly interface.

## Features
- **Scanning for Bluetooth Devices:** Dynamically scans and lists nearby Bluetooth devices.
- **Device Information Display:** Shows details like device name, address, and signal strength.
- **Filtering and Sorting:** Allows users to filter devices by paired/unpaired status and sort by name or signal strength.
- **Real-Time Updating:** Automatically updates the list of devices at regular intervals.
- **Interactive User Interface:** Provides a responsive and intuitive interface for user interactions.
- **Device Connection Capability:** Offers functionality to connect to selected Bluetooth devices.

## Prerequisites
- Python 3.x
- Compatibility with platforms supporting the Kivy framework and Bleak library.

## Installation

### Step 1: Install Python
Ensure Python 3.x is installed on your system. Visit [Python's official website](https://www.python.org/downloads/) for download and installation instructions.

### Step 2: Install Kivy
```bash
pip install kivy
```

### Step 3: Install Bleak
```bash
pip install bleak
```

## Setup Instructions
1. Clone or download the source code from the repository.
2. Navigate to the directory containing the app.
3. Run the app using the Python interpreter:
   ```bash
   python main.py
   ```

## Usage
- **Start a Scan:** Click the scan button to start scanning for Bluetooth devices.
- **Filter and Sort:** Use the provided spinners to filter and sort the device list.
- **Connect to a Device:** Click on the 'Connect' button next to a device to attempt a connection.

## Troubleshooting
For any issues, refer to the Kivy and Bleak documentation, or raise an issue in the repository.

## Contributing
Contributions to the project are welcome. Please refer to the contributing guidelines before making a pull request.

## License
This project is released under [MIT License](https://opensource.org/licenses/MIT).
