#!/bin/bash

# Author: Stephen Cole
# Date: 2024-07-24

# URL of the GitHub file
GITHUB_URL="https://raw.githubusercontent.com/CrowdStrike/falcon-scripts/main/bash/containers/falcon-container-sensor-pull/falcon-container-sensor-pull.sh"

# Extract the filename from the URL
FILENAME=$(basename "$GITHUB_URL")

# Functions

# Get the version number from the downloaded file
get_version() {
  grep '^VERSION=' /tmp/"$FILENAME" | cut -d'=' -f2 | tr -d '"'
}

# Main Script

# Download the file from GitHub and save it to the current directory
# --silent - Supresses standard/error output
# --remote-name - Keeps the original filename when saving
# --location - Follow redirects
curl --silent --remote-name --location "$GITHUB_URL"

# Check if the local file exists
if [ -f "$FILENAME" ]; then
  VERSION=$(get_version)

  # There is a variable in the filename called VERSION
  # If version is empty, use the current date for the backup filename
  if [ -z "$VERSION" ]; then
    VERSION=$(date +%Y%m%d%H%M)
  fi

  # Create a backup filename using the version number or date
  BACKUP_FILENAME="${FILENAME%.*}_backup_$VERSION.${FILENAME##*.}"

  # Backup of the existing file
  mv "$FILENAME" "$BACKUP_FILENAME"

  # Add the backup to a zip archive
  # The -q flag ensures the command runs quietly
  # The -r Updates an existing archive
  zip -q -r backups.zip "$BACKUP_FILENAME"

  # Remove the backup after adding it to the archive
  rm "$BACKUP_FILENAME"

  echo "Backup created: $BACKUP_FILENAME"
  echo "The file on GitHub is newer. Updating the local file."
  mv /tmp/"$FILENAME" "$FILENAME"

  # Make the script executable
  chmod 744 "$FILENAME"

else

  # If the local file doesn't exist, move the downloaded file 
  # from /tmp directory to the local directory
  echo "The local file doesn't exist. Downloading the file."
  mv /tmp/"$FILENAME" "$FILENAME"

  # Make the script executable
  chmod 744 $FILENAME
fi
