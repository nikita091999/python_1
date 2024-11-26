import os
import requests

# Configuration
BASE_RAW_URL = "https://github.com/nikita091999/python_1/blob/main/"  # Base URL for raw content
FILES_TO_UPDATE = ["main.py"]  # Files to download
LOCAL_PATH = "/home/datamann/"  # Local directory to save the files

def download_file(file_name, url, local_path):
    """Download a file from the given URL and save it locally."""
    try:
        print(f"Downloading {file_name}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        file_path = os.path.join(local_path, file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"{file_name} updated successfully!")
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")

def check_and_update_files():
    """Check for updates and download the latest files from the repository."""
    for file_name in FILES_TO_UPDATE:
        file_url = BASE_RAW_URL + file_name
        download_file(file_name, file_url, LOCAL_PATH)

def restart_device():
    """Restart the device."""
    print("Restarting the device...")
    os.system("sudo reboot")

if __name__ == "__main__":
    try:
        print("Checking for updates...")
        check_and_update_files()
        print("All files updated successfully!")
        
        # Restart the device after updates
        restart_device()
    except Exception as e:
        print(f"Error during update: {e}")
