#!/usr/bin/env python3

import subprocess
import sys
import datetime

# Path to the file containing server nicknames and IP addresses
server_file = "/path/to/server_file"

# Path to the log file
log_file = "/path/to/log_file"

# Check if the "s" command was executed with a nickname argument
if len(sys.argv) == 2 and sys.argv[1] != "":
    nickname = sys.argv[1].strip()
    # Initialize the log file with a timestamp
    with open(log_file, "a") as f:
        f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Starting s command\n")
    # Search for the nickname in the server file
    with open(server_file, "r") as f:
        for line in f:
            fields = line.strip().split()
            if len(fields) == 2 and fields[1] == nickname:
                server = fields[0]
                break
        else:
            server = None
    # If the server is found, SSH into it
    if server is not None:
        # Check if SSH key exists
        result = subprocess.run(["ls", "-l", "~/.ssh/id_rsa"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if "No such file or directory" in result.stderr.decode():
            # Generate SSH key
            result = subprocess.run(["ssh-keygen", "-t", "rsa", "-b", "4096", "-f", "~/.ssh/id_rsa", "-N", ""], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                with open(log_file, "a") as f:
                    f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Generated SSH key\n")
            else:
                with open(log_file, "a") as f:
                    f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Failed to generate SSH key\n")
                sys.exit(1)
        # Start ssh-agent and add key
        result = subprocess.run(["eval", "$(ssh-agent -s)"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        if result.returncode == 0:
            result = subprocess.run(["ssh-add", "~/.ssh/id_rsa"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode == 0:
                with open(log_file, "a") as f:
                    f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Added SSH key to ssh-agent\n")
            else:
                with open(log_file, "a") as f:
                    f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Failed to add SSH key to ssh-agent\n")
                sys.exit(1)
        else:
            with open(log_file, "a") as f:
                f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Failed to start ssh-agent\n")
            sys.exit(1)
        # Add key to remote server
        result = subprocess.run(["ssh-copy-id", "-i", "~/.ssh/id_rsa.pub", server], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            with open(log_file, "a") as f:
                f.write(datetime.datetime.now().strftime("%Y-%m-%d % "%H:%M:%S") + " - Added SSH key to remote server\n")
# SSH into server
result = subprocess.run(["ssh", "-q", server], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
if result.returncode == 0:
with open(log_file, "a") as f:
f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" - Connected to server {server}\n")
else:
with open(log_file, "a") as f:
f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" - Failed to connect to server {server}\n")
sys.exit(1)
else:
with open(log_file, "a") as f:
f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + f" - Server not found for nickname {nickname}\n")
sys.exit(1)
else:
print("Usage: s nickname")
with open(log_file, "a") as f:
f.write(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") + " - Usage: s nickname\n")
sys.exit(1)
