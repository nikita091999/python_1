import os
import requests

BASE_RAW_URL = "https://raw.githubusercontent.com/nikita091999/python_1/main/"  # Corrected to RAW URL format
FILES_TO_UPDATE = ["updatefile.py", "config1.json"]  # Files to update
LOCAL_PATH = "/home/datamann/"  # Local path to save the files

def download_file(file_name, url, local_path):
    """
    Download a file from the given URL and save it locally.
    """
    try:
        print(f"Downloading {file_name}...")
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        
        file_path = os.path.join(local_path, file_name)
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"{file_name} updated successfully!")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error while downloading {file_name}: {http_err}")
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")

def check_and_update_files():
    """
    Check for updates and download the latest files from the repository.
    """
    for file_name in FILES_TO_UPDATE:
        file_url = BASE_RAW_URL + file_name
        download_file(file_name, file_url, LOCAL_PATH)

def restart_device():
    """
    Restart the device.
    """
    print("Restarting the device...")
    os.system("sudo reboot")

if __name__ == "__main__":
    try:
        print("Checking for updates...")
        check_and_update_files()
        print("All files updated successfully!")
        
        # Uncomment this line if you want to restart the device after updating
        # restart_device()
    except Exception as e:
        print(f"Error during update: {e}")
