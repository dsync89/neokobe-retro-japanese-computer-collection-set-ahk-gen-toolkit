# Organize the CD rom folders. FD and HD don't need much organization as they are very structured already

import os
import json
import shutil
import re

# Read the configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Get the root_folder_path from the configuration
ROM_DIR = config.get('rom_dir') # the extracted neokobe zip files
OUTPUT_DIR = config.get('output_dir')
EXTRACTED_FD_ROM_DIR = config.get('extracted_fd_rom_dir')
EXTRACTED_HD_ROM_DIR = config.get('extracted_hd_rom_dir')
EXTRACTED_CD_ROM_DIR = config.get('extracted_cd_rom_dir')

# ---
rom_dirs = [ EXTRACTED_FD_ROM_DIR, EXTRACTED_HD_ROM_DIR ]

# FD and HD are easier to process, just remove the suffix [FD] or [HD]
for index, rom_dir in enumerate(rom_dirs):
    suffixToRemove = ''
    if index == 0: # FD
        suffixToRemove = ' [FD]'  
    elif index == 1:
        suffixToRemove = ' [HD]'

    directories = [d for d in os.listdir(rom_dir) if os.path.isdir(os.path.join(rom_dir, d))]

    for directory in directories:
        if directory.endswith(suffixToRemove):
            source_path = os.path.join(rom_dir, directory)
            destination_path = os.path.join(rom_dir, directory.replace(suffixToRemove, "").strip())

            os.rename(source_path, destination_path)
            print(f"Renamed {source_path} to {destination_path}")

# CD require additonal complexity of processing because of the different suffix
rom_dirs = [ EXTRACTED_CD_ROM_DIR ]

for rom_dir in rom_dirs:

    directories = [d for d in os.listdir(rom_dir) if os.path.isdir(os.path.join(rom_dir, d))]

    for directory in directories:    
        with open("gametitles\\gametitle_cd.txt", 'r') as file:
            # Iterate through each line in the file
            for line in file:
                gameTitle = line.strip().replace('\n', '')
                if gameTitle in directory: # finding match

                    source_directory = os.path.join(rom_dir, directory)
                    destination_directory = os.path.join(rom_dir, gameTitle)

                    if not os.path.exists(destination_directory):
                        os.makedirs(destination_directory) 
                    
                    # Move each file to the destination directory
                    for file_name in os.listdir(source_directory):
                        source_file = os.path.join(source_directory, file_name)
                        if os.path.isfile(source_file):  # Ensure it's a file (not directory)
                            destination_file = os.path.join(destination_directory, file_name)
                            print("Moving {} ==> {}".format(source_file, destination_file))

                            shutil.move(source_file, destination_file)
                            print("Moved {} ==> {}".format(source_file, destination_file))

                    # remove the folder after moved
                    shutil.rmtree(source_directory)
                    print("Removed folder: {}".format(source_directory))

                    break # move on to the next folder