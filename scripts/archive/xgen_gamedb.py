# generate a .gamedb.txt file that list all the files in each game folder as a row in the format of
# GAMETITLE | FILE 1 | FILE 2 | FILE 3 ...

import os
import json

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
    
    rom_dirs = [  EXTRACTED_HD_ROM_DIR]

    for rom_dir in rom_dirs:
        root_folder_path = rom_dir
        output_file_path = os.path.join(root_folder_path, '.gamedb.txt')

        directories = [d for d in os.listdir(root_folder_path) if os.path.isdir(os.path.join(root_folder_path, d))]

        with open(output_file_path, 'w') as output_file:
            for directory in directories:
                folder_path = os.path.join(root_folder_path, directory)
                files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
                
                boot_media_files = []

                for file in files:
                    root, extension = os.path.splitext(file)
                    if extension.lower() in  ('.bin', '.img', '.slh', '.sub'): # exclude file with these file extensions
                        # print("Skipping file extension: {}".format(extension.lower()))
                        continue

                    boot_media_files.append(file)
            
                output_file.write(f"{directory} | {' | '.join(boot_media_files)}\n")

        print("Saved .gamedb to: {}".format(output_file_path))
