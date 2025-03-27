import urequests
import os
import machine
import time

# GitHub API URL to list repo contents
GITHUB_API_URL = "https://api.github.com/repos/UJJWALKHANNAL/ESPP/contents/"
# Base URL for raw file downloads
BASE_URL = "https://raw.githubusercontent.com/UJJWALKHANNAL/ESPP/main/"

# Download and update all files
def download_and_update():
    try:
        print("Fetching file list from GitHub...")

        # Get file list from GitHub API
        response = urequests.get(GITHUB_API_URL)

        if response.status_code == 200:
            file_list = response.json()
            for file_info in file_list:
                if file_info["type"] == "file":
                    file_name = file_info["name"]
                    download_file(file_name)
        else:
            print(f"Failed to fetch file list. Status code: {response.status_code}")
    except Exception as e:
        print(f"Error fetching file list: {e}")

# Download individual files
def download_file(file_name):
    try:
        url = BASE_URL + file_name
        print(f"Checking {file_name} for updates...")

        # Fetch content from GitHub
        response = urequests.get(url)

        if response.status_code == 200:
            with open(file_name, "w") as f:
                f.write(response.text)
            print(f"{file_name} updated successfully!")
        else:
            print(f"Failed to download {file_name}. Status code: {response.status_code}")

        response.close()
    except Exception as e:
        print(f"Error updating {file_name}: {e}")

# Run updates and restart
def run_update():
    download_and_update()
    print("Restarting ESP to apply updates...")
    time.sleep(2)
    machine.reset()

# Run update on boot
run_update()
