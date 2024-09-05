# Tailscaling
TailScale tools

# device-manager.py
# Tailscale Device Manager

Tailscale Device Manager is a command-line tool for managing devices in your Tailscale network. It allows you to list devices, remove old devices, and remove specific devices using the Tailscale API.

## Features

- List all devices in your Tailscale network
- Remove devices that haven't been seen for a specified number of days
- Remove a specific device by its ID

## Prerequisites

- Python 3.6 or higher
- A Tailscale account with an API key

## Installation

1. Clone this repository or download the script:
```
   git clone https://github.com/yourusername/tailscale-device-manager.git
   cd tailscale-device-manager
```
2. Install the required Python packages:
```
   pip install requests python-dateutil
```
## Usage

The script requires a Tailscale API key for authentication. You can pass this key using the --api-key option or by setting the TAILSCALE_API_KEY environment variable.

### List all devices

To list all devices in your Tailscale network:
```
python tailscale_device_manager.py --api-key YOUR_API_KEY --list
```
### Remove old devices

To remove devices that haven't been seen for a specified number of days:
```
python tailscale_device_manager.py --api-key YOUR_API_KEY --remove-old DAYS
```
Replace DAYS with the number of days of inactivity after which a device should be removed.

### Remove a specific device

To remove a specific device by its ID:
```
python tailscale_device_manager.py --api-key YOUR_API_KEY --remove DEVICE_ID
```
Replace DEVICE_ID with the ID of the device you want to remove.

## Examples

1. List all devices:
   ```
   python tailscale_device_manager.py --api-key abcdef1234567890 --list
   ```
3. Remove devices not seen in the last 60 days:
   ```
   python tailscale_device_manager.py --api-key abcdef1234567890 --remove-old 60
   ```
5. Remove a specific device:
   ```
   python tailscale_device_manager.py --api-key abcdef1234567890 --remove tsdev-1234567890abcdef
   ```
## Security Note

This script requires a Tailscale API key with permissions to read device information and remove devices. Handle this key securely and avoid sharing it or committing it to version control.
