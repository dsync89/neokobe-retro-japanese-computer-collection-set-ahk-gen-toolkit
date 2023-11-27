# add additional key map per game from `keymapper\gametitle` folder.

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

SEP = '; ============================================================\n'

def add_keymap(keymap_file_path, game_ahk_file_path):

    # list all 
    with open(keymap_file_path, 'r') as file1:
        content_file1 = file1.read()

    with open(game_ahk_file_path, 'r') as file2:
        content_file2 = file2.read()

    if content_file1 not in content_file2:
        print("Adding keymap file: {} to game AHK file: {}".format(keymap_file_path, game_ahk_file_path))

        with open(game_ahk_file_path, 'a') as file2:
            file2.write("\n")
            file2.write("\n")
            file2.write(SEP)
            file2.write("; Key Bindings imported from {}\n".format(keymap_file_path))
            file2.write(SEP)
            file2.write(content_file1)   

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
if __name__ == "__main__":
    print_config()

    rom_dirs = [ EXTRACTED_FD_ROM_DIR, EXTRACTED_HD_ROM_DIR, EXTRACTED_CD_ROM_DIR]

    for index, rom_dir in enumerate(rom_dirs):
        media_type = ''
        if index == 0: # fd
            media_type = 'fd'
            KEYMAP_DIR = "keymapping\\fd"
        elif index == 1: # hd
            media_type = 'hd'          
            KEYMAP_DIR = "keymapping\\hd"
        elif index == 2: # cd
            media_type = 'cd'          
            KEYMAP_DIR = "keymapping\\cd"            
        else:
            print("Invalid index!")
            exit(1)

        GAME_DIR = rom_dirs[index]       

        keymap_ahk_files = [f for f in os.listdir(KEYMAP_DIR) if f.endswith('.ahk')]

        print("Found {} keymap files for media type: {}".format(len(keymap_ahk_files), media_type.upper()))

        game_ahk_files = [f for f in os.listdir(GAME_DIR) if f.endswith('.ahk')]

        # 1. apply global keymap to all games
        print("Applying global keymap to {} AHK scripts...".format(len(game_ahk_files)))
        for game_ahk_file in game_ahk_files:
            game_ahk_file_path = os.path.join(GAME_DIR, game_ahk_file)
            add_keymap(os.path.join(KEYMAP_DIR, 'global.ahk'), game_ahk_file_path)

        print()
        # 2. apply game specific keymap to the matching game
        print("Applying game specific keymap to matching AHK scripts...")
        for game_ahk_file in game_ahk_files:
            game_ahk_file_path = os.path.join(GAME_DIR, game_ahk_file)
            for keymap_ahk_file in keymap_ahk_files:            
                if keymap_ahk_file == game_ahk_file:
                    keymap_ahk_file_path = os.path.join(KEYMAP_DIR, keymap_ahk_file)
                    add_keymap(keymap_ahk_file_path, game_ahk_file_path)



        # for keymap_ahk_file in keymap_ahk_files:
        #     print("    {}".format(keymap_ahk_file))

        #     # add game specific keymap        
        #     game_ahk_files = [f for f in os.listdir(GAME_DIR) if f.endswith('.ahk')]

        #     for game_ahk_file in game_ahk_files:
        #         game_ahk_file_path = os.path.join(GAME_DIR, game_ahk_file)
        #         add_keymap(os.path.join(KEYMAP_DIR, 'global.ahk'), game_ahk_file_path)

        #         if keymap_ahk_file == game_ahk_file:
        #             keymap_ahk_file_path = os.path.join(KEYMAP_DIR, keymap_ahk_file)
        #             add_keymap(keymap_ahk_file_path, game_ahk_file_path)

        print()