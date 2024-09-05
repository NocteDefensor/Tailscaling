import argparse
import requests
from datetime import datetime, timedelta
import sys
from dateutil.parser import parse
from dateutil.tz import tzutc
import json

BASE_URL = "https://api.tailscale.com/api/v2"

def get_devices(api_key):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(f"{BASE_URL}/tailnet/-/devices", headers=headers)
    response.raise_for_status()
    return response.json()["devices"]

def list_devices(api_key):
    devices = get_devices(api_key)
    for device in devices:
        print(f"Hostname: {device['hostname']}")
        print(f"ID: {device['id']}")
        print(f"Last Seen: {device['lastSeen']}")
        print(f"OS: {device['os']}")
        print(f"Tags: {', '.join(device.get('tags', []))}")
        print("---")

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

def get_device(api_key, device_id):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.get(f"{BASE_URL}/device/{device_id}", headers=headers)
    response.raise_for_status()
    return response.json()

def list_tags(api_key, device_id):
    device = get_device(api_key, device_id)
    tags = device.get('tags', [])
    if tags:
        print(f"Tags for device {device_id}:")
        for tag in tags:
            print(f"- {tag}")
    else:
        print(f"No tags found for device {device_id}")

def update_device_tags(api_key, device_id, tags, action):
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    # Get current device information
    try:
        response = requests.get(f"{BASE_URL}/device/{device_id}", headers=headers)
        response.raise_for_status()
        device = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error getting device information: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return

    current_tags = set(device.get('tags', []))
    
    if action == 'remove':
        if len(current_tags) == 0:
            print(f"Error: Device {device_id} has no tags to remove.")
            return
        elif len(current_tags) == 1:
            print(f"Error: Device {device_id} only has one tag. You cannot remove the last tag from a device.")
            print(f"Current tag: {list(current_tags)[0]}")
            return
    
    if action == 'add':
        new_tags = list(current_tags.union(set(tags)))
    elif action == 'remove':
        tags_to_remove = set(tags)
        new_tags = list(current_tags - tags_to_remove)
    
    # Ensure all tags start with "tag:"
    new_tags = ["tag:" + tag if not tag.startswith("tag:") else tag for tag in new_tags]
    
    # Prepare the update data
    update_data = {
        "tags": new_tags
    }
    
    # Update the device tags
    try:
        response = requests.post(f"{BASE_URL}/device/{device_id}/tags", headers=headers, json=update_data)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error updating device tags: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return

    # Verify the changes
    try:
        response = requests.get(f"{BASE_URL}/device/{device_id}", headers=headers)
        response.raise_for_status()
        updated_device = response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error verifying tag changes: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"Response content: {e.response.text}")
        return

    updated_tags = set(updated_device.get('tags', []))
    
    if action == 'add':
        added_tags = updated_tags - current_tags
        if added_tags:
            print(f"Tags added successfully to device {device_id}: {', '.join(added_tags)}")
        else:
            print(f"No new tags were added to device {device_id}. They may already exist.")
    else:  # remove
        removed_tags = current_tags - updated_tags
        if removed_tags:
            print(f"Tags removed successfully from device {device_id}: {', '.join(removed_tags)}")
        else:
            print(f"No tags were removed from device {device_id}. They may not exist.")
    
    print(f"Current tags for device {device_id}: {', '.join(updated_tags)}")

def add_tags(api_key, device_id, tags):
    tag_list = ["tag:" + tag if not tag.startswith("tag:") else tag for tag in tags.split(',')]
    update_device_tags(api_key, device_id, tag_list, 'add')

def remove_tags(api_key, device_id, tags):
    tag_list = ["tag:" + tag if not tag.startswith("tag:") else tag for tag in tags.split(',')]
    update_device_tags(api_key, device_id, tag_list, 'remove')

def find_devices(api_key, search_term):
    devices = get_devices(api_key)
    found_devices = [device for device in devices if search_term.lower() in device['hostname'].lower()]
    
    if found_devices:
        print(f"Found {len(found_devices)} device(s) matching '{search_term}':")
        for device in found_devices:
            print(f"Hostname: {device['hostname']}")
            print(f"ID: {device['id']}")
            print(f"Last Seen: {device['lastSeen']}")
            print(f"OS: {device['os']}")
            print(f"Tags: {', '.join(device.get('tags', []))}")
            print("---")
    else:
        print(f"No devices found matching '{search_term}'")

def main():
    parser = argparse.ArgumentParser(description="Tailscale Device Manager")
    parser.add_argument("--api-key", required=True, help="Tailscale API key")
    parser.add_argument("--remove-old", type=int, metavar="DAYS", help="Remove devices older than specified number of days")
    parser.add_argument("--list", action="store_true", help="List all devices")
    parser.add_argument("--remove", help="Remove a specific device by ID")
    parser.add_argument("--list-tags", help="List tags for a specific device by ID")
    parser.add_argument("--add-tags", nargs=2, metavar=("DEVICE_ID", "TAGS"), help="Add tags to a device")
    parser.add_argument("--remove-tags", nargs=2, metavar=("DEVICE_ID", "TAGS"), help="Remove tags from a device")
    parser.add_argument("--find-device", help="Find devices with specified words or characters in hostname")

    args = parser.parse_args()

    try:
        if args.remove_old is not None:
            remove_old_devices(args.api_key, args.remove_old)
        elif args.list:
            list_devices(args.api_key)
        elif args.remove:
            remove_device(args.api_key, args.remove)
        elif args.list_tags:
            list_tags(args.api_key, args.list_tags)
        elif args.add_tags:
            add_tags(args.api_key, args.add_tags[0], args.add_tags[1])
        elif args.remove_tags:
            remove_tags(args.api_key, args.remove_tags[0], args.remove_tags[1])
        elif args.find_device:
            find_devices(args.api_key, args.find_device)
        else:
            print("Please specify an action: --remove-old DAYS, --list, --remove DEVICE_ID, --list-tags DEVICE_ID, --add-tags DEVICE_ID TAGS, --remove-tags DEVICE_ID TAGS, or --find-device SEARCH_TERM")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
