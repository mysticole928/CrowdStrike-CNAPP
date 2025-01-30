#!/usr/bin/env python3

""""
Falcon Container Sensor Pull Script Updater

This script checks for the latest version of the Falcon Container Sensor Pull script from
CrowdStrike's GitHub repository. If a newer version is available, it downloads and updates
the script in the current directory.

Functionality:
- Determines if the `falcon-container-sensor-pull.sh` script is present in the current directory.
- Extracts the local version (if available) from the `VERSION` variable in the script.
- Fetches the latest version of the script from GitHub without downloading it entirely.
- Compares the local and remote versions.
- If the script is missing or outdated, prompts the user before downloading the latest version.
- Ensures the downloaded script is executable (`chmod +x`).
- Provides error handling for network issues or missing version numbers.

Usage:
1. Run the script directly:  python3 update_falcon_pull.py
2. To automate the update without modifying the path, create an alias in `~/.zshrc` or `~/.bashrc`:
- alias update-falcon="python3 ~/.scripts/update_falcon_pull.py"

Dependencies:
- Python 3.x
- `requests` library (install with `pip install requests`)

Author: Stephen Cole
Date: 2025-01-30
"""

import os
import re
import requests
import stat

# GitHub URL of the script
GITHUB_URL = "https://raw.githubusercontent.com/CrowdStrike/falcon-scripts/main/bash/containers/falcon-container-sensor-pull/falcon-container-sensor-pull.sh"
FILENAME = os.path.basename(GITHUB_URL)
LOCAL_SCRIPT = os.path.join(os.getcwd(), FILENAME)

def fetch_remote_version():
    """Fetches the remote script and extracts the VERSION variable."""
    try:
        response = requests.get(GITHUB_URL, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"Error fetching remote script: {e}")
        return None
    
    match = re.search(r'VERSION="([\d\.]+)"', response.text)
    return match.group(1) if match else None

def fetch_local_version():
    """Extracts the VERSION variable from the local script if it exists."""
    if not os.path.exists(LOCAL_SCRIPT):
        return None
    
    try:
        with open(LOCAL_SCRIPT, "r", encoding="utf-8") as file:
            for line in file:
                match = re.search(r'VERSION="([\d\.]+)"', line)
                if match:
                    return match.group(1)
    except Exception as e:
        print(f"Error reading local script: {e}")
        return None

def download_script():
    """Downloads the latest version of the script."""
    try:
        response = requests.get(GITHUB_URL, timeout=10)
        response.raise_for_status()
        with open(LOCAL_SCRIPT, "w", encoding="utf-8") as file:
            file.write(response.text)
        
        # Make the file executable
        os.chmod(LOCAL_SCRIPT, os.stat(LOCAL_SCRIPT).st_mode | stat.S_IEXEC)
        print(f"Updated {FILENAME} to version {fetch_remote_version()} in {os.getcwd()}.")
    except requests.RequestException as e:
        print(f"Error downloading script: {e}")

def confirm_directory():
    """Asks user if they want to download the script in the current directory."""
    print(f"The Falcon Container Sensor Pull script was not found in:\n  {os.getcwd()}\n")
    response = input("Do you want to download it here? (y/N) ").strip().lower()
    if response == 'y':
        return True
    print("Exiting without changes.")
    return False

def main():
    """Main logic to compare versions and update the script if necessary."""
    local_version = fetch_local_version()
    remote_version = fetch_remote_version()

    if remote_version is None:
        print("Error: Unable to determine the remote version from GitHub.")
        return
    
    if local_version is None:
        if confirm_directory():
            print(f"Downloading {FILENAME} (Version {remote_version}) to {os.getcwd()}...")
            download_script()
        return
    
    if local_version == remote_version:
        print(f"The latest version ({remote_version}) is already available in {os.getcwd()}. No update needed.")
    else:
        print(f"Updating {FILENAME} from version {local_version} to {remote_version} in {os.getcwd()}...")
        download_script()

if __name__ == "__main__":
    main()
