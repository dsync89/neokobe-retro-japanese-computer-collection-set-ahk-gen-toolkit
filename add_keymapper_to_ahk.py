# add additional key map per game from `keymapper\gametitle` folder.

import os
import sys
import json
import shutil

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

    else:   
        print("Skipping adding keymap file: {} to game AHK file: {} because content is the same!".format(keymap_file_path, game_ahk_file_path))

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <ROM_DIR> <KEYMAP_DIR>")
        exit(1)
    else:
        GAME_DIR = sys.argv[1]        
        KEYMAP_DIR = sys.argv[2]  

    keymap_ahk_files = [f for f in os.listdir(KEYMAP_DIR) if f.endswith('.ahk')]

    print("Found {} keymap files".format(len(keymap_ahk_files)))

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

    print()