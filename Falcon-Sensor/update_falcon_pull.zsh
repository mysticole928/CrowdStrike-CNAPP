#!/bin/zsh

# URL of the Falcon Container Sensor Pull script
GITHUB_URL="https://raw.githubusercontent.com/CrowdStrike/falcon-scripts/main/bash/containers/falcon-container-sensor-pull/falcon-container-sensor-pull.sh"
FILENAME=${GITHUB_URL:t}  # Extract filename from URL
LOCAL_SCRIPT="./$FILENAME"

# Function to extract the VERSION variable from a file
extract_version() {
    grep -m1 'VERSION="' "$1" 2>/dev/null | awk -F'"' '{print $2}' | tr -d '\r' | xargs
}

# Get current working directory
CURRENT_DIR=$(pwd)

# Check if the file exists in the current directory
if [[ -f "$LOCAL_SCRIPT" ]]; then
    LOCAL_VERSION=$(extract_version "$LOCAL_SCRIPT")
else
    LOCAL_VERSION="none"
fi

# If the script isn't found, ask for confirmation before proceeding
if [[ "$LOCAL_VERSION" == "none" ]]; then
    echo "The Falcon Container Sensor Pull script was not found in:"
    echo "  $CURRENT_DIR"
    echo ""
    read -q "RESPONSE?Do you want to download it here? (y/N) "
    echo ""  # Move to a new line after input
    case "$RESPONSE" in
        [Yy]*) echo "Proceeding with download..." ;;
        *) echo "Exiting without changes."; exit 0 ;;
    esac
fi

# Fetch the remote version without downloading the full file
REMOTE_VERSION=$(curl --silent "$GITHUB_URL" | grep -m1 'VERSION="' | awk -F'"' '{print $2}' | tr -d '\r' | xargs)

# Error handling for missing version numbers
if [[ -z "$REMOTE_VERSION" ]]; then
    echo "Error: Unable to determine the remote version from GitHub."
    exit 1
fi

if [[ "$LOCAL_VERSION" == "none" ]]; then
    echo "Downloading $FILENAME (Version $REMOTE_VERSION) to $CURRENT_DIR..."
elif [[ -z "$LOCAL_VERSION" ]]; then
    echo "Error: Unable to determine the local version."
    exit 1
elif [[ "$LOCAL_VERSION" == "$REMOTE_VERSION" ]]; then
    echo "The latest version ($REMOTE_VERSION) is already available in $CURRENT_DIR. No update needed."
    exit 0
else
    echo "Updating $FILENAME from version $LOCAL_VERSION to $REMOTE_VERSION in $CURRENT_DIR..."
fi

# Download the latest version to the current directory
curl --silent --location --output "$LOCAL_SCRIPT" "$GITHUB_URL"

# Make it executable
chmod 744 "$LOCAL_SCRIPT"

echo "Updated $FILENAME to version $REMOTE_VERSION in $CURRENT_DIR."
exit 0
