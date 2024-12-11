import os
import requests
import shutil
import subprocess as sp
import time
import json

BASE_RAW_URL = "https://raw.githubusercontent.com/nikita091999/python_1/main/"
DEPOSIT_DIR = "/home/datamann/deposit"
MAIN_DIR = "/home/datamann/main"
FILES_TO_UPDATE = ["update.py", "config1.json", "version.json"]
VERSION_FILE = os.path.join(MAIN_DIR, "version.json")

def ensure_directories():
    for directory in [DEPOSIT_DIR, MAIN_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created missing directory: {directory}")

def download_file(file_name, url, dest_dir):
    try:
        print(f"Downloading {file_name} from {url}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        dest_path = os.path.join(dest_dir, file_name)
        with open(dest_path, "wb") as file:
            file.write(response.content)
        print(f"Updated: {file_name}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error while updating {file_name}: {http_err}")
    except Exception as e:
        print(f"Error updating {file_name}: {e}")

def get_current_version():
    if os.path.exists(VERSION_FILE):
        with open(VERSION_FILE, "r") as file:
            version_data = json.load(file)
            return version_data.get("version", "")
    return ""

def update_version():
    # Check the latest version from the server
    raw_url = BASE_RAW_URL + "version.json"
    response = requests.get(raw_url, timeout=10)
    if response.status_code == 200:
        latest_version_data = response.json()
        latest_version = latest_version_data.get("version", "")
        current_version = get_current_version()

        if latest_version != current_version:
            print(f"New version found: {latest_version}. Updating files...")
            # Download the new files only if version is updated
            for file_name in FILES_TO_UPDATE:
                download_file(file_name, BASE_RAW_URL + file_name, MAIN_DIR)
            # Update the version
            with open(VERSION_FILE, "w") as file:
                json.dump(latest_version_data, file, indent=4)
            print("Version updated successfully.")
        else:
            print("No new version available. Skipping update.")
    else:
        print(f"Failed to fetch version information from {raw_url}")

def start_updatefile():
    updatefile_script = os.path.join(MAIN_DIR, "update.py")
    if os.path.exists(updatefile_script):
        print("Starting update.py...")
        return sp.Popen(["python3", updatefile_script], cwd=MAIN_DIR)
    else:
        raise FileNotFoundError(f"{updatefile_script} not found!")

def monitor_and_update():
    ensure_directories()

    while True:
        try:
            # Check for version updates and download the necessary files
            update_version()

            # Start the updatefile.py script
            update_proc = start_updatefile()

            while update_proc.poll() is None:
                print("Running update.py. Checking for updates in the background...")
                time.sleep(60)
                update_version()  # Check for updates periodically

            print("updatefile.py process has stopped. Restarting with updated files...")
        except FileNotFoundError as e:
            print(e)
            time.sleep(10)  # Retry after 10 seconds if updatefile.py not found
        except Exception as e:
            print(f"Error during monitoring: {e}")
        finally:
            time.sleep(5)

if __name__ == "__main__":
    monitor_and_update()
