#!/usr/bin/env python3

# 2024-01-26 
#
# Simple python3 script that will process all the yaml files in the
# current directory and run: kubectl delete -f <filename>
#
# For outputs, it prints the command, standard out, and standard error.
#
# It's meant for tearing down a lab environment.  If there is no pod
# running, it will just move on to the next one.
#
# There is no error checking, logging, or warranty in this script.

import glob
import os
import subprocess

from pathlib import Path

CWD = os.getcwd()


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


CWD = Path('.')


def get_yaml_filenames(directory):
    """List generator of yaml files in a directory"""
    for file in CWD.glob('**/*.yaml'):
        yield (file)


def main():
    clear()
    try:
        for file in get_yaml_filenames(CWD):
            print(f'kubectl delete -f {file}')
            result = subprocess.run(
                ["kubectl", "delete", "-f", file], capture_output=True, text=True)
            print(f'Standard Out: {result.stdout}')
            print(f'Standard Error {result.stderr}')

    except Exception as e:
        print(f'Exception: {e}')
        pass


if __name__ == "__main__":
    main()
