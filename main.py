import os
import requests

BASE_RAW_URL = "https://github.com/nikita091999/python_1/blob/main/"  
FILES_TO_UPDATE = ["main.py","config1.json"]  
LOCAL_PATH = "/home/datamann/"  

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
        
        restart_device()
    except Exception as e:
        print(f"Error during update: {e}")
        ####____###
# import cv2
# import time
# import os
# import json
# import base64
# import requests
# import schedule
# import ftplib
# from datetime import datetime

# # Load the JSON configuration file
# def load_config(file_path="Ras_device.json"):
#     try:
#         with open(file_path, "r") as file:
#             config = json.load(file)
#         return config
#     except Exception as e:
#         print(f"Error loading configuration file: {e}")
#         return None

# # Generate basic authentication credentials
# def gen_basic_credential(username, password):
#     return 'Basic {}'.format(base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8'))

# # Ensure folder structure exists locally
# def ensure_local_folder_structure(base_dir, camera_id, timestamp):
#     folder_path = os.path.join(
#         base_dir,
#         camera_id,
#         timestamp.strftime("%Y"),
#         timestamp.strftime("%m"),
#         timestamp.strftime("%d"),
#         timestamp.strftime("%H")
#     )
#     os.makedirs(folder_path, exist_ok=True)
#     return folder_path

# # Ensure FTP folder structure exists
# def ensure_ftp_folder_structure(ftp, folder_path):
#     path_parts = folder_path.split("/")
#     for part in path_parts:
#         try:
#             ftp.cwd(part)
#         except ftplib.error_perm:
#             ftp.mkd(part)
#             ftp.cwd(part)

# # Upload file to FTP server
# def upload_to_ftp(file_path, remote_folder, ftp_config):
#     FTP_HOSTNAME = ftp_config['FTP_HOSTNAME']
#     FTP_USERNAME = ftp_config['FTP_USERNAME']
#     FTP_PASSWORD = ftp_config['FTP_PASSWORD']

#     try:
#         ftp_server = ftplib.FTP(FTP_HOSTNAME, FTP_USERNAME, FTP_PASSWORD)
#         ftp_server.encoding = "utf-8"

#         # Ensure the folder structure exists on FTP server
#         ensure_ftp_folder_structure(ftp_server, remote_folder)

#         # Upload file with original filename
#         file_name = os.path.basename(file_path)
#         with open(file_path, "rb") as file:
#             ftp_server.storbinary(f"STOR {file_name}", file)
#         print(f"Uploaded file: {file_name}")

#         ftp_server.quit()
#     except Exception as e:
#         print(f"Error uploading to FTP: {e}")

# # Capture snapshot from a camera
# def capture_snapshot(camera, config):
#     base_dir = config["camera_file_format"]["sd_base_dir"]
#     file_extension = config["camera_file_format"]["file_extension"]
#     camera_id = camera["id"]
#     timestamp = datetime.now()

#     # Ensure local folder structure
#     folder_path = ensure_local_folder_structure(base_dir, camera_id, timestamp)
#     filename = f"{timestamp.strftime('%Y%m%d%H%M')}{file_extension}"
#     file_path = os.path.join(folder_path, filename)

#     if camera["type"] == "RTSP":
#         cap = cv2.VideoCapture(camera["url"], cv2.CAP_FFMPEG)
#         if not cap.isOpened():
#             print(f"Error: Unable to connect to RTSP stream for camera {camera_id}")
#             return

#         try:
#             ret, frame = cap.read()
#             if not ret or frame is None:
#                 print(f"Error: Failed to retrieve frame for camera {camera_id}")
#                 return

#             cv2.imwrite(file_path, frame)
#             print(f"RTSP Snapshot saved locally: {file_path}")

#         except Exception as e:
#             print(f"Error capturing RTSP snapshot for camera {camera_id}: {e}")
#         finally:
#             cap.release()

#     elif camera["type"] == "NVR":
#         headers = {'Authorization': gen_basic_credential(camera["username"], camera["password"])}
#         try:
#             response = requests.get(camera["url"], headers=headers, timeout=20)
#             if response.status_code == 200:
#                 with open(file_path, "wb") as file:
#                     file.write(response.content)
#                 print(f"NVR Snapshot saved locally: {file_path}")
#             else:
#                 print(f"Failed to capture NVR snapshot for camera {camera_id}. Status code: {response.status_code}")
#         except Exception as e:
#             print(f"Error capturing NVR snapshot for camera {camera_id}: {e}")

#     # Convert folder path for FTP upload
#     remote_folder = folder_path.replace(base_dir, config['ftp']['base_folder']).replace("\\", "/")
#     upload_to_ftp(file_path, remote_folder, config['ftp'])

# # Start scheduled tasks for all cameras
# def start_scheduled_tasks(config):
#     for camera in config["cameras"]:
#         schedule.every(1).minutes.do(capture_snapshot, camera=camera, config=config)

#     print("Scheduled tasks started...")
#     while True:
#         schedule.run_pending()
#         time.sleep(1)

# # Main logic
# config = load_config()
# if config:
#     start_scheduled_tasks(config)
# else:
#     print("Configuration loading failed. Exiting.")



import cv2
import time
import os
import json
import base64
import requests
import schedule
import ftplib
from datetime import datetime, timedelta

# Load the JSON configuration file
def load_config(file_path="Ras_device.json"):
    try:
        with open(file_path, "r") as file:
            config = json.load(file)
        return config
    except Exception as e:
        print(f"Error loading configuration file: {e}")
        return None

# Generate basic authentication credentials
def gen_basic_credential(username, password):
    return 'Basic {}'.format(base64.b64encode(f'{username}:{password}'.encode('utf-8')).decode('utf-8'))

# Ensure folder structure exists locally
def ensure_local_folder_structure(base_dir, camera_id, timestamp):
    folder_path = os.path.join(
        base_dir,
        camera_id,
        timestamp.strftime("%Y"),
        timestamp.strftime("%m"),
        timestamp.strftime("%d"),
        timestamp.strftime("%H")
    )
    os.makedirs(folder_path, exist_ok=True)
    return folder_path

# Ensure FTP folder structure exists
def ensure_ftp_folder_structure(ftp, folder_path):
    path_parts = folder_path.split("/")
    for part in path_parts:
        try:
            ftp.cwd(part)
        except ftplib.error_perm:
            ftp.mkd(part)
            ftp.cwd(part)

# Upload file to FTP server
def upload_to_ftp(file_path, remote_folder, ftp_config):
    FTP_HOSTNAME = ftp_config['FTP_HOSTNAME']
    FTP_USERNAME = ftp_config['FTP_USERNAME']
    FTP_PASSWORD = ftp_config['FTP_PASSWORD']

    try:
        ftp_server = ftplib.FTP(FTP_HOSTNAME, FTP_USERNAME, FTP_PASSWORD)
        ftp_server.encoding = "utf-8"

        # Ensure the folder structure exists on FTP server
        ensure_ftp_folder_structure(ftp_server, remote_folder)

        # Upload file with original filename
        file_name = os.path.basename(file_path)
        with open(file_path, "rb") as file:
            ftp_server.storbinary(f"STOR {file_name}", file)
        print(f"Uploaded file: {file_name}")

        ftp_server.quit()
    except Exception as e:
        print(f"Error uploading to FTP: {e}")

# Capture snapshot from a camera
def capture_snapshot(camera, config):
    base_dir = config["camera_file_format"]["sd_base_dir"]
    file_extension = config["camera_file_format"]["file_extension"]
    camera_id = camera["id"]
    timestamp = datetime.now()

    # Ensure local folder structure
    folder_path = ensure_local_folder_structure(base_dir, camera_id, timestamp)
    filename = f"{timestamp.strftime('%Y%m%d%H%M')}{file_extension}"
    file_path = os.path.join(folder_path, filename)

    if camera["type"] == "RTSP":
        cap = cv2.VideoCapture(camera["url"], cv2.CAP_FFMPEG)
        if not cap.isOpened():
            print(f"Error: Unable to connect to RTSP stream for camera {camera_id}")
            return

        try:
            ret, frame = cap.read()
            if not ret or frame is None:
                print(f"Error: Failed to retrieve frame for camera {camera_id}")
                return

            cv2.imwrite(file_path, frame)
            print(f"RTSP Snapshot saved locally: {file_path}")

        except Exception as e:
            print(f"Error capturing RTSP snapshot for camera {camera_id}: {e}")
        finally:
            cap.release()

    elif camera["type"] == "NVR":
        headers = {'Authorization': gen_basic_credential(camera["username"], camera["password"])}
        try:
            response = requests.get(camera["url"], headers=headers, timeout=20)
            if response.status_code == 200:
                with open(file_path, "wb") as file:
                    file.write(response.content)
                print(f"NVR Snapshot saved locally: {file_path}")
            else:
                print(f"Failed to capture NVR snapshot for camera {camera_id}. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error capturing NVR snapshot for camera {camera_id}: {e}")

    # Convert folder path for FTP upload
    remote_folder = folder_path.replace(base_dir, config['ftp']['base_folder']).replace("\\", "/")
    upload_to_ftp(file_path, remote_folder, config['ftp'])

# Start scheduled tasks for all cameras
def start_scheduled_tasks(config):
    for camera_config in config["cameras"]:
        schedule.every(1).minute.do(capture_snapshot, camera=camera_config, config=config)

    # Daily check for the previous day
    def daily_check():
        prev_day_folder = os.path.join(
            '/home/datamann/log/VMS',
            (datetime.now() - timedelta(days=1)).strftime("%Y"),
            (datetime.now() - timedelta(days=1)).strftime("%m"),
            (datetime.now() - timedelta(days=1)).strftime("%d")
        )
        prev_day_remote = os.path.join(
            config['ftp']['base_folder'], "VMS",
            (datetime.now() - timedelta(days=1)).strftime("%Y"),
            (datetime.now() - timedelta(days=1)).strftime("%m"),
            (datetime.now() - timedelta(days=1)).strftime("%d")
        ).replace("\\", "/")

        print(f"[DEBUG] Daily Check: Local folder: {prev_day_folder}")
        print(f"[DEBUG] Daily Check: Remote folder: {prev_day_remote}")
        try:
            check_missing_snapshots(folder_path=prev_day_folder, remote_folder=prev_day_remote, ftp_config=config['ftp'])
        except Exception as e:
            print(f"[ERROR] Daily check failed: {e}")

    schedule.every().day.at("00:01").do(daily_check)

    # Hourly check
    def hourly_check():
        prev_hour_folder = os.path.join(
            '/home/datamann/log/VMS',
            datetime.now().strftime("%Y"),
            datetime.now().strftime("%m"),
            datetime.now().strftime("%d"),
            (datetime.now() - timedelta(hours=1)).strftime("%H")
        )
        prev_hour_remote = os.path.join(
            config['ftp']['base_folder'], "VMS",
            datetime.now().strftime("%Y"),
            datetime.now().strftime("%m"),
            datetime.now().strftime("%d"),
            (datetime.now() - timedelta(hours=1)).strftime("%H")
        ).replace("\\", "/")

        print(f"[DEBUG] Hourly Check: Local folder: {prev_hour_folder}")
        print(f"[DEBUG] Hourly Check: Remote folder: {prev_hour_remote}")
        try:
            check_missing_snapshots(folder_path=prev_hour_folder, remote_folder=prev_hour_remote, ftp_config=config['ftp'])
        except Exception as e:
            print(f"[ERROR] Hourly check failed: {e}")

    schedule.every().hour.at(":01").do(hourly_check)

    print("[INFO] Scheduled tasks started...")
    while True:
        try:
            schedule.run_pending()
            time.sleep(1)
        except Exception as e:
            print(f"[ERROR] Error in scheduled task execution: {e}")

# Function to check for missing snapshots between local and FTP folder
def check_missing_snapshots(folder_path, remote_folder, ftp_config):
    try:
        # List files in the local folder
        local_files = os.listdir(folder_path)
        local_files = [f for f in local_files if f.endswith('.jpg')]  # Only JPG files
        
        # Connect to FTP server and list files in the remote folder
        ftp_server = ftplib.FTP(ftp_config['FTP_HOSTNAME'], ftp_config['FTP_USERNAME'], ftp_config['FTP_PASSWORD'])
        ftp_server.encoding = "utf-8"
        ftp_server.cwd(remote_folder)
        remote_files = ftp_server.nlst()
        
        # Compare the files in both directories
        missing_files = [f for f in local_files if f not in remote_files]
        
        if missing_files:
            print(f"Missing files: {missing_files}")
            for file in missing_files:
                file_path = os.path.join(folder_path, file)
                upload_to_ftp(file_path, remote_folder, ftp_config)  # Upload the missing file
        else:
            print(f"All files are uploaded. No missing files found.")
            
        ftp_server.quit()
    except Exception as e:
        print(f"Error during missing file check: {e}")

# Main logic
config = load_config()
if config:
    start_scheduled_tasks(config)
else:
    print("Configuration loading failed. Exiting.")

