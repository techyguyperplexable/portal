import json
import requests

# URL to fetch the list of device JSON data
data_source_url = "https://raw.githubusercontent.com/RisingOS-Revived-devices/RisingOS_Web/refs/heads/main/fetch.json"
output_file = "devices.json"
error_log_file = "error.log"

error_count = 0

def log_error(message):
    """Log errors to a file and increment error counter."""
    global error_count
    error_count += 1
    with open(error_log_file, "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")

def fetch_json(url):
    """Fetch JSON data from a URL."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        log_error(f"Error fetching {url}: {e}")
        return None

def fetch_device_data(url, base_info):
    """Fetch device information from a given JSON URL."""
    data = fetch_json(url)
    if not data or "response" not in data or not isinstance(data["response"], list) or not data["response"]:
        log_error(f"Unexpected JSON structure in {url}")
        return None

    device_info = data["response"][0]  # Assume first item contains relevant data

    return {
        "status": base_info.get("status", ""),
        "oem": base_info.get("oem", ""),
        "device": base_info.get("device", ""),
        "codename": base_info.get("codename", url.split("/")[-1].replace(".json", "")),
        "maintainer": base_info.get("maintainer", ""),
        "variant": "VANILLA" if "VANILLA" in url else "CORE" if "CORE" in url else "GAPPS",
        "download": device_info.get("download", ""),
        "paypal": device_info.get("paypal", ""),
        "device_avatar": base_info.get("device_avatar", ""),
        "maintainer_avatar": base_info.get("maintainer_avatar", ""),
        "filesize": device_info.get("size", 0),  # Fetch correct filesize field
        "md5": device_info.get("md5", ""),
        "sha256": device_info.get("sha256", ""),
        "device_changelog": base_info.get("device_changelog", ""),
        "version": device_info.get("version", ""),
        "buildtype": device_info.get("buildtype", ""),
        "recovery": device_info.get("recovery", ""),
        "timestamp": device_info.get("timestamp", "")
    }

def main():
    """Main function to fetch URLs and process device data."""
    global error_count
    error_count = 0  # Reset error count at start

    # Clear previous log
    open(error_log_file, "w").close()

    devices_data = fetch_json(data_source_url)
    if not devices_data:
        log_error("Failed to retrieve data from data source.")
        print("Failed to retrieve data. Check error.log for details.")
        return

    devices = []
    for base_codename, base_info in devices_data.items():
        if "urls" in base_info:
            for url in base_info["urls"]:
                device_data = fetch_device_data(url, base_info)
                if device_data:
                    devices.append(device_data)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(devices, f, indent=4, ensure_ascii=False)

    print(f"Data saved to {output_file}")
    print(f"Total errors encountered: {error_count}. Check {error_log_file} for details.")

if __name__ == "__main__":
    main()
