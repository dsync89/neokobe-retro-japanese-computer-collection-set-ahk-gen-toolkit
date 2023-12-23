# Create AHK file for each game titles

import os
import json
import shutil

# Read the configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Get the root_folder_path from the configuration
ROM_DIR = config.get('rom_dir') # the extracted neokobe zip files

GAMEDB_TXT_OVERWRITE = config.get('gamedb_overwrite_file')

def print_config():
    print("-------------------------")
    print("Program Config:")
    print("-------------------------")   
    print("ROM_DIR: {}".format(ROM_DIR))
    print("GAMEDB_TXT_OVERWRITE: {}".format(GAMEDB_TXT_OVERWRITE))
    print()

def remove_ahk_not_needed(file_path):
    lines = []
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("File not found!")
    
    for index, line in enumerate(lines):    
        index = index+1
        ahk_file = "{}.ahk".format(line.strip())
        source_ahk_filepath = os.path.join(ROM_DIR, ahk_file)
        print("Removing AHK file [{}/{}]: {}".format(index, len(lines), source_ahk_filepath));
        if os.path.exists(source_ahk_filepath):
            os.remove(source_ahk_filepath)
            print(f"File '{source_ahk_filepath}' has been successfully removed.")
        else:
            pass

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
if __name__ == "__main__":
    print_config()


    root_folder_path = ROM_DIR
    output_file_path = root_folder_path

    def list_folders(dir):    
        folders = []
        # Get all immediate directories (folders) in the parent folder
        directories = [d for d in os.listdir(dir) if os.path.isdir(os.path.join(dir, d))]

        # Print the list of immediate directories
        print("List of immediate directories:")
        for directory in directories:
            print(directory)    
            folders.append(directory)
        return folders

    shutil.copy("./templates/.config.ini", output_file_path)

    # get a list of folder
    folder_list = list_folders(root_folder_path)

    # copy AHK template and rename it as the same as folder name
    for _ in folder_list:
        ahk_filename = "{}.ahk".format(os.path.join(output_file_path, _))

        print(ahk_filename)
        
        # select different ahk template based on media type
        ahk_template = "./templates/ahkv2/gametitle.ahk"

        print("Copying AHK template from {} ==> {}".format(ahk_template, ahk_filename))
        shutil.copy(ahk_template, ahk_filename)

    # remove AHK files that are not needed, as they are probably HD that need
    # to run a CD titles, which already taken care of by gamedb overwrite list
    ahk_to_remove_filepath = '.\\gametitles\\ahk_to_remove.txt'
    print("Deleting AHK files from {}".format(ahk_to_remove_filepath))        
    remove_ahk_not_needed(ahk_to_remove_filepath)