#!/usr/bin/env python3
"""
This script prints the installed version of Visual Studio Code.
"""

import subprocess
import sys

def get_vscode_version():
    """Get the VS Code version by running the 'code --version' command"""
    try:
        # Run the 'code --version' command and capture the result
        result = subprocess.run(['code', '--version'], 
                               capture_output=True, 
                               text=True, 
                               check=True)
        
        # The result contains the version on the first line
        version_info = result.stdout.strip().split('\n')
        version = version_info[0] if version_info else "Could not retrieve version"
        
        return version
    except subprocess.CalledProcessError:
        return "Error: Could not run 'code --version'"
    except FileNotFoundError:
        return "Error: VS Code is not available in PATH"

if __name__ == "__main__":
    version = get_vscode_version()
    print(f"{version}")