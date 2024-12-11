import os
import requests
import shutil
import subprocess as sp
import time

BASE_RAW_URL = "https://raw.githubusercontent.com/nikita091999/python_1/main/"
DEPOSIT_DIR = "/home/datamann/deposit"
MAIN_DIR = "/home/datamann/main"
FILES_TO_UPDATE = ["updatefile.py", "config1.json"]

# Ensure required directories exist
def ensure_directories():
    for directory in [DEPOSIT_DIR, MAIN_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created missing directory: {directory}")

# Download files from GitHub
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

# Update specified files
def update_files():
    for file_name in FILES_TO_UPDATE:
        raw_url = BASE_RAW_URL + file_name
        download_file(file_name, raw_url, MAIN_DIR)

# Start updatefile.py
def start_updatefile():
    update_script = os.path.join(MAIN_DIR, "updatefile.py")
    if os.path.exists(update_script):
        print("Starting updatefile.py...")
        return sp.Popen(["python3", update_script], cwd=MAIN_DIR)
    else:
        raise FileNotFoundError(f"{update_script} not found!")

# Monitor updatefile.py and perform updates
def monitor_and_update():
    ensure_directories()
    update_files()

    while True:
        try:
            main_proc = start_updatefile()

            while main_proc.poll() is None:
                print("Running updatefile.py. Checking for updates in the background...")
                time.sleep(60)  # Check for updates every 60 seconds
                update_files()

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
