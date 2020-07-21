#!/usr/bin/env python3

import os
import subprocess

from datetime import date, datetime, timedelta
from shutil import copyfile
from utils import bash_source_file, format_date, get_env_var, growl_notification, set_icon


excluded_paths = " Archive"

desktop_dir = os.path.expanduser('~/Desktop')
scruffy_dir = os.path.dirname(os.path.realpath(__file__))
scruffy_config = os.path.expanduser('~/.scruffyrc')

if not os.path.exists(scruffy_config):
    copyfile(f"{scruffy_dir}/.scruffyrc.default", scruffy_config)

bash_source_file(scruffy_config)

DAYS_TO_LEAVE_ON_DESKTOP = get_env_var(
    "SCRUFFY_DAYS_TO_LEAVE_ON_DESKTOP",
    default=3,
    data_type=int,
)
DAYS_TO_CHECK_FOR_REQUIRED_ARCHIVE = get_env_var(
    "SCRUFFY_DAYS_TO_CHECK_FOR_REQUIRED_ARCHIVE",
    default=90,
    data_type=int,
)
SOUND_ON_COMPLETE = get_env_var(
    "SCRUFFY_SOUND_ON_COMPLETE",
    default="Purr",
)
UNMOUNT_DISK_IMAGES = get_env_var(
    "SCRUFFY_UNMOUNT_DISK_IMAGES",
    default=False,
    data_type=bool,
)

print("\n✨🧹 cleaning up your desktop...\n")

today = date.today()
todays_folder = format_date(today)
recent_dates = [
    format_date(today - timedelta(n))
    for n in range(DAYS_TO_CHECK_FOR_REQUIRED_ARCHIVE)
]

# Clean up items on the desktop
desktop_list = os.listdir(desktop_dir)
for file in desktop_list:
    if file not in recent_dates and file not in excluded_paths:
        print(f"Archiving {desktop_dir}/{file}...")

        file_stat = os.stat(f"{desktop_dir}/{file}")
        modified = format_date(datetime.fromtimestamp(file_stat.st_mtime))

        if not os.path.exists(f"{desktop_dir}/{modified}"):
            print(f"Creating daily folder {modified}...")

            # Try to create folder with no spaces to set icon, then rename
            if not os.path.exists(f"{desktop_dir}/{str(file_stat.st_mtime)}"):
                os.mkdir(f"{desktop_dir}/{str(file_stat.st_mtime)}")
                set_icon(
                    filename=f"{desktop_dir}/{str(file_stat.st_mtime)}",
                    icon=f"{scruffy_dir}/assets/leaf.png",
                )
                os.rename(
                    f"{desktop_dir}/{str(file_stat.st_mtime)}",
                    f"{desktop_dir}/{modified}"
                )
            else:
                os.mkdir(f"{desktop_dir}/{modified}")

        if os.path.exists(f"{desktop_dir}/{modified}/{file}"):
            index = 2
            filename = file.rsplit('.', 1)

            while os.path.exists(f"{desktop_dir}/{modified}/{filename[0]}-{index}.{filename[1]}"):
                index += 1
            print(f"File {desktop_dir}/{file} exists in archive - saving as {file}-{index}")
            os.rename(
                f"{desktop_dir}/{file}",
                f"{desktop_dir}/{modified}/{filename[0]}-{index}.{filename[1]}",
            )
        else:
            os.rename(
                f"{desktop_dir}/{file}",
                f"{desktop_dir}/{modified}/{file}",
            )

# Archive old daily folders
if not os.path.exists(f"{desktop_dir}/ Archive"):
    print("Making \" Archive\" folder for old days...")
    os.mkdir(f"{desktop_dir}/ Archive")

old_folders = [
    format_date(today - timedelta(n))
    for n in range(DAYS_TO_LEAVE_ON_DESKTOP, DAYS_TO_CHECK_FOR_REQUIRED_ARCHIVE)
]
files_archived = 0
for folder in old_folders:
    if os.path.exists(f"{desktop_dir}/{folder}"):
        print(f"Archiving daily folder {desktop_dir}/{folder}")
        os.rename(
            f"{desktop_dir}/{folder}",
            f"{desktop_dir}/ Archive/{folder}",
        )
        files_archived += 1
if not files_archived:
    print("No files found to clean up.")

print("")

growl_notification(
    title="Scruffy Complete!",
    text="What a clean desktop you have ✨🧹",
    sound=SOUND_ON_COMPLETE,
)
# Unmount disk images
if UNMOUNT_DISK_IMAGES:
    mounted_images = subprocess.getoutput("diskutil list | grep \"disk image\"")
    if mounted_images:
        mounted_images = mounted_images.replace(" (disk image):", "")
        mounted_images = mounted_images.split("\n")

        for image in mounted_images:
            print(f"Unmounting {image}")
            os.system(f"diskutil unmountDisk {image}")

print("\n✅ All done!\n")
