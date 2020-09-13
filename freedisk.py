import os
import shutil

# Directory in which files should be deleted
folder = '/home/pi/Videos'
files = []

# Minimum free disk space in bytes
minfree = 3000000000
currfree = shutil.disk_usage(folder).free

# If enough free disk space: nothing to do -> exit program
if currfree > minfree: exit()

# Calc amount of bytes to free on disk
tofree = minfree - currfree

# Get list of files in folder
for f in os.listdir(folder):
  stat = os.stat(os.path.join(folder, f))
  files.append([os.path.join(folder, f), stat.st_mtime, stat.st_size])
# and store information in list like [filename, modification time, size]

# Sort file list by modification time
files.sort(key=lambda i: i[1], reverse=True)

# Delete files - oldest first - until minimum disk space is reached
while files and tofree > 0:
  delfile = files.pop()
  os.remove(delfile[0])
  tofree -= delfile[2]