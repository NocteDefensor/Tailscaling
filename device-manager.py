import argparse
import requests
from datetime import datetime, timedelta
import sys
from dateutil.parser import parse
from dateutil.tz import tzutc

BASE_URL = "https://api.tailscale.com/api/v2"

def get_devices(api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(f"{BASE_URL}/tailnet/-/devices", headers=headers)
    response.raise_for_status()
    return response.json()["devices"]

def remove_device(api_key, device_id):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.delete(f"{BASE_URL}/device/{device_id}", headers=headers)
    response.raise_for_status()
    print(f"Device {device_id} removed successfully.")

def remove_old_devices(api_key, days):
    devices = get_devices(api_key)
    current_time = datetime.now(tzutc())
    removed_count = 0
    for device in devices:
        last_seen = parse(device["lastSeen"])
        if (current_time - last_seen) > timedelta(days=days):
            print(f"Removing device: {device['hostname']} (ID: {device['id']}, Last seen: {last_seen})")
            remove_device(api_key, device['id'])
            removed_count += 1
    print(f"Removed {removed_count} device(s) older than {days} days.")

def list_devices(api_key):
    devices = get_devices(api_key)
    for device in devices:
        print(f"Hostname: {device['hostname']}")
        print(f"ID: {device['id']}")
        print(f"Last Seen: {device['lastSeen']}")
        print(f"OS: {device['os']}")
        print("---")

def main():
    parser = argparse.ArgumentParser(description="Tailscale Device Manager")
    parser.add_argument("--api-key", required=True, help="Tailscale API key")
    parser.add_argument("--remove-old", type=int, metavar="DAYS", help="Remove devices older than specified number of days")
    parser.add_argument("--list", action="store_true", help="List all devices")
    parser.add_argument("--remove", help="Remove a specific device by ID")

    args = parser.parse_args()

    try:
        if args.remove_old is not None:
            remove_old_devices(args.api_key, args.remove_old)
        elif args.list:
            list_devices(args.api_key)
        elif args.remove:
            remove_device(args.api_key, args.remove)
        else:
            print("Please specify an action: --remove-old DAYS, --list, or --remove DEVICE_ID")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
