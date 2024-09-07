# Tailscaling
TailScale tools

# device-manager.py
# Tailscale Device Manager

Tailscale Device Manager is a command-line tool for managing devices in your Tailscale network. It allows you to list devices, remove old devices, manage tags, and search for devices using the Tailscale API.

## Features

- List all devices in your Tailscale network
- Remove devices that haven't been seen for a specified number of days
- Remove a specific device by its ID
- List tags for a specific device
- Add tags to a device
- Remove tags from a device
- Find devices by partial hostname match

## Prerequisites

- Python 3.6 or higher
- A Tailscale account with an API key

## Installation

1. Clone this repository or download the script:

   ```
   git clone https://github.com/NocteDefensor/Tailscaling.git
   cd Tailscaling
   ```

2. Install the required Python packages:

   ```
   pip install requests python-dateutil
   ```

## Usage

The script will prompt you for your Tailscale API key when you run any command. This ensures that your API key is not stored in your command line history.

### List all devices

To list all devices in your Tailscale network:

```
python3 device-manager.py --list
```

### Remove old devices

To remove devices that haven't been seen for a specified number of days:

```
python3 device-manager.py --remove-old DAYS
```

Replace `DAYS` with the number of days of inactivity after which a device should be removed.

### Remove a specific device

To remove a specific device by its ID:

```
python3 device-manager.py --remove DEVICE_ID
```

Replace `DEVICE_ID` with the ID of the device you want to remove.

### List tags for a device

To list tags for a specific device:

```
python3 device-manager.py --list-tags DEVICE_ID
```

Replace `DEVICE_ID` with the ID of the device you want to list tags for.

### Add tags to a device

To add tags to a specific device:

```
python3 device-manager.py --add-tags DEVICE_ID "tag1,tag2,tag3"
```

Replace `DEVICE_ID` with the ID of the device you want to add tags to, and provide a comma-separated list of tags.

### Remove tags from a device

To remove tags from a specific device:

```
python3 device-manager.py --remove-tags DEVICE_ID "tag1,tag2,tag3"
```

Replace `DEVICE_ID` with the ID of the device you want to remove tags from, and provide a comma-separated list of tags to remove.

### Find devices by hostname

To find devices by partial hostname match:

```
python3 device-manager.py --find-device SEARCH_TERM
```

Replace `SEARCH_TERM` with the partial hostname you want to search for.

## Examples

1. List all devices:
   ```
   python3 device-manager.py --list
   ```

2. Remove devices not seen in the last 60 days:
   ```
   python3 device-manager.py --remove-old 60
   ```

3. Remove a specific device:
   ```
   python3 device-manager.py --remove tsdev-1234567890abcdef
   ```

4. List tags for a device:
   ```
   python3 device-manager.py --list-tags tsdev-1234567890abcdef
   ```

5. Add tags to a device:
   ```
   python3 device-manager.py --add-tags tsdev-1234567890abcdef "tag1,tag2"
   ```

6. Remove tags from a device:
   ```
   python3 device-manager.py --remove-tags tsdev-1234567890abcdef "tag1,tag2"
   ```

7. Find devices with "laptop" in the hostname:
   ```
   python3 device-manager.py --find-device laptop
   ```

For each command, you will be prompted to enter your Tailscale API key securely.

## Security Note

This script requires a Tailscale API key with permissions to read device information, remove devices, and manage tags. The API key is input securely at runtime and is not stored or logged. However, always ensure you're using the script in a secure environment.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

