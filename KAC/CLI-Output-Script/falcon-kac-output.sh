#!/bin/bash
#
# 2024-07-23
#
# This script processes the warning and error message output from 
# Falcon Kubernetes Admission Controller and makes it easier to read
# in the terminal.
#
# It also appends the output to a logfile.
# 
# It was designed to work with the output of kubectl.
#
# If the script is in the local dirctory:
#
# kubectl apply -f deployment_file_name.yaml 2>&1 | ./falcon-kac-output.sh
#
# The redirection ( 2>&1 ) and script name can be cumbersome.  
#
# There's a way make it easier: 
#
# Create an alias with a nested function. The script stays local *and* it
# avoids issue with the $PATH
#
# In this example, the script is in a directory with the path: ~/scripts
#
# alias kapply="function _kapply(){ kubectl apply -f \$1 2>&1 | ~/scripts/falcon-kac-output.sh; }; _kapply"
#
# To use it:
# 
#   kapply kubernetes-resource-file.yaml
# 
# Put the alias in your .zshrc or .bash_profile and it will always be available.

# Assign the logfile name
logfile="falcon-kac-output.log"

# Get the current timestamp
timestamp=$(date +"%Y-%m-%d - %H:%M:%S")

# Function to display usage information
usage() {
    echo "This script formats the output from the CrowdStrike"
    echo "Falcon Admission Controller."
    echo
    echo "Usage:" 
    echo "\t\$ kubectl apply -f <input_file>.yaml 2>&1 | $0"
    echo "\t\$ kubectl create -f <input_file>.yaml 2>&1 | $0"
    echo
    exit 1
}

# Verify command was run correctly
if [ -t 0 ]; then
    usage
fi

# Read input from stdin
input=$(cat)

# Define ANSI color codes
RED='\033[0;31m'
YELLOW='\033[1;33m'
BRIGHT_GREEN='\033[1;32m'
WARNING='\033[30;43m'
ERROR='\033[30;41m'
NC='\033[0m' # No Color

# Define a function to format the output
falcon_kac_output() {
    echo "Falcon KAC Output" | tee -a "$logfile"
    echo -e "${YELLOW}==================${NC}" | tee -a "$logfile"
    echo -e "${YELLOW}$timestamp${NC}" | tee -a "$logfile"
    echo -e "${YELLOW}==================${NC}" | tee -a "$logfile"
    echo "$input" | awk -v red="$RED" \
                        -v yellow="$YELLOW" \
                        -v green="$BRIGHT_GREEN" \
                        -v warning="$WARNING" \
                        -v error="$ERROR" \
                        -v nc="$NC" '
    BEGIN {
        warnings = 0
        errors = 0
    }
    /Warning:/ {
        warnings = 1
        # Extract and print the warnings
        sub(/Warning: [0-9]+ warning(s?) from admission webhook "validating.falcon-kac.crowdstrike.com": /, "")
        split($0, warning_messages, ",")
        for (i in warning_messages) {
            gsub(/^[ \t]+|[ \t]+$/, "", warning_messages[i])
            sub(/\{"container: /, yellow "\n\tContainer: " green, warning_messages[i])
            sub(/\"\}$/, "", warning_messages[i])
            print warning "Warning" nc " " warning_messages[i] nc
            print yellow "------------------" nc
        }
    }
    /Error from server/ {
        errors = 1
        # Extract and print the errors
        sub(/Error from server \(Forbidden\): error when creating "[^"]+": admission webhook "validating.falcon-kac.crowdstrike.com" denied the request: /, "")
        split($0, error_messages, ",")
        for (i in error_messages) {
            gsub(/^[ \t]+|[ \t]+$/, "", error_messages[i])
            sub(/\{"container: /, yellow "\n\tContainer: " green, error_messages[i])
            sub(/\"\}$/, "", error_messages[i])
            print error "Error" nc " " error_messages[i] nc
            print red "------------------" nc
        }
    }
    END {
        if (warnings == 0 && errors == 0) {
            print "No warnings or errors found.  Nice!"
        }
    }' | tee -a "$logfile"
}

# Call the function to format the output
falcon_kac_output
