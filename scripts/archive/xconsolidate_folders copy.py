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
# rom_dirs = [ EXTRACTED_FD_ROM_DIR, EXTRACTED_HD_ROM_DIR, EXTRACTED_CD_ROM_DIR]

rom_dirs = [ EXTRACTED_CD_ROM_DIR]

def strip_square_bracket(string):
    return string.split('[', 1)[0].strip()

def strip_ellipses(string):
    if string.endswith('...'):
        return string[:-3].rstrip()
    else:
        return string

def flatten_folder(directory):
    # Traverse the directory tree
    for root, dirs, files in os.walk(directory):
        # Move files to the parent directory
        for file in files:
            try:
                file_path = os.path.join(root, file)
                shutil.move(file_path, directory)
            except:
                pass

    # Remove empty subdirectories
    for root, dirs, files in os.walk(directory, topdown=False):
        for name in dirs:
            os.rmdir(os.path.join(root, name))

for rom_dir in rom_dirs:

    directories = [d for d in os.listdir(rom_dir) if os.path.isdir(os.path.join(rom_dir, d))]

    # 1st pass: remove char till first occurance of '['
    for directory in directories:        
        directory_renamed = strip_square_bracket(directory)
        directory_renamed = strip_ellipses(directory_renamed)

        # Construct full paths for the folders
        current_folder_path = os.path.join(rom_dir, directory)
        new_folder_path = os.path.join(rom_dir, directory_renamed)

        # Check if the current folder exists before renaming
        if os.path.exists(current_folder_path):
            shutil.move(current_folder_path, new_folder_path)
            print(f"Renamed folder '{current_folder_path}' ==> '{new_folder_path}'")
        else:
            print(f"Folder '{current_folder_path}' does not exist in '{rom_dir}'")        

    print()

    # 2nd pass: remove (CD version)
    print("[2nd pass]: Remove (CD version)")    
    directories = [d for d in os.listdir(rom_dir) if os.path.isdir(os.path.join(rom_dir, d))] # rescan the dir again
    for directory in directories:        
        if '(CD version)' in directory:
            directory_renamed = re.sub(r'\s*\(CD version\)', '', directory)

            # move all the files in that folder to the existing one
            source_directory = os.path.join(rom_dir, directory)
            destination_directory = os.path.join(rom_dir, directory_renamed)

            if not os.path.exists(destination_directory):
                os.makedirs(destination_directory)

            # Move each file to the destination directory
            for file_name in os.listdir(source_directory):
                source_file = os.path.join(source_directory, file_name)
                if os.path.isfile(source_file):  # Ensure it's a file (not directory)
                    destination_file = os.path.join(destination_directory, file_name)
                    shutil.move(source_file, destination_file)
                    print("Moving {} ==> {}".format(source_file, destination_file))

            # remove the folder
            shutil.rmtree(source_directory)
            print("Removed folder: {}".format(source_directory))

    
    # lastly, flatten the folder and remove subdirectories
    directories = [d for d in os.listdir(rom_dir) if os.path.isdir(os.path.join(rom_dir, d))]
    for directory in directories:        
        target_dir = os.path.join(rom_dir, directory)
        print("Flatting folder: {}".format(target_dir))
        flatten_folder(target_dir)