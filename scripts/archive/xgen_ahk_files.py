# Create AHK file for each game titles

import os
import json
import shutil

# Read the configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

# Get the root_folder_path from the configuration
ROM_DIR = config.get('rom_dir') # the extracted neokobe zip files

EXTRACTED_FD_ROM_DIR = config.get('extracted_fd_rom_dir')
EXTRACTED_HD_ROM_DIR = config.get('extracted_hd_rom_dir')
EXTRACTED_CD_ROM_DIR = config.get('extracted_cd_rom_dir')

GAMEDB_FD_TXT_OVERWRITE = config.get('gamedb_fd_overwrite_file')
GAMEDB_HD_TXT_OVERWRITE = config.get('gamedb_hd_overwrite_file')
GAMEDB_CD_TXT_OVERWRITE = config.get('gamedb_cd_overwrite_file')

def print_config():
    print("-------------------------")
    print("Program Config:")
    print("-------------------------")   
    print("ROM_DIR: {}".format(ROM_DIR))
    print("EXTRACTED_FD_ROM_DIR: {}".format(EXTRACTED_FD_ROM_DIR))
    print("EXTRACTED_HD_ROM_DIR: {}".format(EXTRACTED_HD_ROM_DIR))
    print("EXTRACTED_CD_ROM_DIR: {}".format(EXTRACTED_CD_ROM_DIR))
    print("GAMEDB_FD_TXT_OVERWRITE: {}".format(GAMEDB_FD_TXT_OVERWRITE))
    print("GAMEDB_HD_TXT_OVERWRITE: {}".format(GAMEDB_HD_TXT_OVERWRITE))
    print("GAMEDB_CD_TXT_OVERWRITE: {}".format(GAMEDB_CD_TXT_OVERWRITE))
    print()


# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
if __name__ == "__main__":
    print_config()

    rom_dirs = [ EXTRACTED_HD_ROM_DIR ]

    for index, rom_dir in enumerate(rom_dirs):
        root_folder_path = rom_dir
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
            ahk_template = ''
            if index == 0: # fd
                ahk_template = "./templates/ahkv2/gametitle_hd.ahk"
            elif index == 1: # hd
                ahk_template = "./templates/ahkv2/gametitle_hd.ahk"
            elif index == 2: # cd
                ahk_template = "./templates/ahkv2/gametitle_cd.ahk"

            print("Copying AHK template from {} ==> {}".format(ahk_template, ahk_filename))
            shutil.copy(ahk_template, ahk_filename)
