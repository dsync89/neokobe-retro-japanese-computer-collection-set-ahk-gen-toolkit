# Overwrite existing .gamedb.txt with user overrides. Useful especially if a game has multiple .hdm files, and 
# you want to specify a particular one, e.g. HDD with 'Installed' keyword should be preferred over 'Cleaned'

# You typically only modify the entry if the game refuse to boot, typical error is 'no system files found'

# You should ONLY run this script after you run gen_gamedb.py once!
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

    # ---
    rom_dirs = [ EXTRACTED_FD_ROM_DIR, EXTRACTED_HD_ROM_DIR, EXTRACTED_CD_ROM_DIR]

    for index, rom_dir in enumerate(rom_dirs):
        if index == 0: # fd
            GAMEDB_TXT_OVERWRITE = GAMEDB_FD_TXT_OVERWRITE
        elif index == 1: # hd
            GAMEDB_TXT_OVERWRITE = GAMEDB_HD_TXT_OVERWRITE
        elif index == 2: # cd
            GAMEDB_TXT_OVERWRITE = GAMEDB_CD_TXT_OVERWRITE
        else:
            print("Invalid index!")
            exit(1)

        gameDbFile = os.path.join(rom_dir, '.gamedb.txt')
        gameDbFileCopy = os.path.join(rom_dir, '.gamedb.txt.orig')

        # only make copy if not exist, we don't want to overwrite the original .gamedb
        if not os.path.exists(gameDbFileCopy): 
            shutil.copyfile(gameDbFile, gameDbFileCopy)
        
        if not os.path.exists(gameDbFile):
            print(".gamedb.txt not found in {}!".format(gameDbFile))
            print("Make sure you run gen_gamedb.py first!")
            exit(1)

        # Read content from the first file
        with open(gameDbFile, 'r') as file1:
            lines_file1 = file1.readlines()

        # Read content from the second file
        with open(GAMEDB_TXT_OVERWRITE, 'r') as file2:
            lines_file2 = file2.readlines()

        # Mapping identifiers (first columns) to lines from file 2
        file2_map = {line.split('|')[0].strip(): line for line in lines_file2}

        # Update lines in file 1 if identifier matches from file 2
        for index, line in enumerate(lines_file1):
            identifier = line.split('|')[0].strip()
            if identifier in file2_map:
                lines_file1[index] = file2_map[identifier]

        # Write the updated content back to file 1
        with open(gameDbFile, 'w') as file1:
            file1.writelines(lines_file1)
            print("Replacing lines in {} with user specified overrides {}".format(gameDbFile, GAMEDB_TXT_OVERWRITE))