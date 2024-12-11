import os
import requests
import shutil
import subprocess as sp
import time

BASE_RAW_URL = "https://raw.githubusercontent.com/nikita091999/python_1/main/"
DEPOSIT_DIR = "/home/datamann/deposit"
MAIN_DIR = "/home/datamann/main"
FILES_TO_UPDATE = ["updatefile.py", "config1.json"]

def ensure_directories():
    """Ensure the required directories exist."""
    for directory in [DEPOSIT_DIR, MAIN_DIR]:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"Created missing directory: {directory}")

def download_file(file_name, url, dest_dir):
    """Download a file from a URL and save it in the destination directory."""
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

def update_files():
    """Update all files listed in FILES_TO_UPDATE."""
    for file_name in FILES_TO_UPDATE:
        raw_url = BASE_RAW_URL + file_name
        download_file(file_name, raw_url, MAIN_DIR)

def start_update_script():
    """Run updatefile.py if it exists."""
    update_script = os.path.join(MAIN_DIR, "updatefile.py")
    if os.path.exists(update_script):
        print("Running updatefile.py...")
        sp.run(["python3", update_script], cwd=MAIN_DIR, check=True)
    else:
        print("updatefile.py not found. Skipping.")

def start_main():
    """Start the main.py script."""
    main_script = os.path.join(MAIN_DIR, "main.py")
    if os.path.exists(main_script):
        print("Starting main.py...")
        return sp.Popen(["python3", main_script], cwd=MAIN_DIR)
    else:
        raise FileNotFoundError(f"{main_script} not found!")

def monitor_and_update():
    """Monitor and update scripts, restarting main.py as needed."""
    ensure_directories()
    update_files()

    while True:
        try:
            start_update_script()  # Ensure updatefile.py is run
            main_proc = start_main()

            while main_proc.poll() is None:
                print("Running main.py. Checking for updates in the background...")
                time.sleep(60)
                update_files()

            print("main.py process has stopped. Restarting with updated files...")
        except FileNotFoundError as e:
            print(e)
            time.sleep(10)  # Retry after 10 seconds if main.py not found
        except Exception as e:
            print(f"Error during monitoring: {e}")
        finally:
            time.sleep(5)

if __name__ == "__main__":
    monitor_and_update()
