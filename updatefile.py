# import os
# import requests

# BASE_RAW_URL = "https://raw.githubusercontent.com/nikita091999/python_1/main/"  # Corrected to RAW URL format
# FILES_TO_UPDATE = ["updatefile.py", "config1.json"]  # Files to update
# LOCAL_PATH = "/home/datamann/"  # Local path to save the files

# def download_file(file_name, url, local_path):
#     """
#     Download a file from the given URL and save it locally.
#     """
#     try:
#         print(f"Downloading {file_name}...")
#         response = requests.get(url, timeout=10)
#         response.raise_for_status()
        
#         file_path = os.path.join(local_path, file_name)
#         with open(file_path, "wb") as file:
#             file.write(response.content)
#         print(f"{file_name} updated successfully!")
#     except requests.exceptions.HTTPError as http_err:
#         print(f"HTTP error while downloading {file_name}: {http_err}")
#     except Exception as e:
#         print(f"Error downloading {file_name}: {e}")

# def check_and_update_files():
#     """
#     Check for updates and download the latest files from the repository.
#     """
#     for file_name in FILES_TO_UPDATE:
#         file_url = BASE_RAW_URL + file_name
#         download_file(file_name, file_url, LOCAL_PATH)

# def restart_device():
#     """
#     Restart the device.
#     """
#     print("Restarting the device...")
#     os.system("sudo reboot")

# if __name__ == "__main__":
#     try:
#         print("Checking for updates...")
#         check_and_update_files()
#         print("All files updated successfully!")
        
#         # Uncomment this line if you want to restart the device after updating
#         # restart_device()
#     except Exception as e:
#         print(f"Error during update: {e}")



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
        # Check if file content has changed
        if os.path.exists(file_path):
            with open(file_path, "rb") as existing_file:
                if existing_file.read() == response.content:
                    print(f"{file_name} is already up-to-date.")
                    return False  # No update required

        # Write new content to file
        with open(file_path, "wb") as file:
            file.write(response.content)
        print(f"{file_name} updated successfully!")
        return True  # File was updated
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error while downloading {file_name}: {http_err}")
    except Exception as e:
        print(f"Error downloading {file_name}: {e}")
    return False  # Failed to update file

def check_and_update_files():
    """
    Check for updates and download the latest files from the repository.
    Returns True if any file was updated, otherwise False.
    """
    updated = False
    for file_name in FILES_TO_UPDATE:
        file_url = BASE_RAW_URL + file_name
        if download_file(file_name, file_url, LOCAL_PATH):
            updated = True
    return updated

def restart_device():
    """
    Restart the device.
    """
    print("Restarting the device...")
    os.system("sudo reboot")

if __name__ == "__main__":
    try:
        print("Checking for updates...")
        if check_and_update_files():
            print("Updates detected. Restarting the device...")
            restart_device()
        else:
            print("No updates were required. Device will not restart.")
    except Exception as e:
        print(f"Error during update: {e}")
