# Overwrite existing .gamedb.txt with user overrides. Useful especially if a game has multiple .hdm files, and 
# you want to specify a particular one, e.g. HDD with 'Installed' keyword should be preferred over 'Cleaned'

# You typically only modify the entry if the game refuse to boot, typical error is 'no system files found'

# You should ONLY run this script after you run gen_gamedb.py once!
import os
import sys
import json
import shutil

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python script.py <ROM_DIR> <GAMEDB_TXT_OVERWRITE_PATH>")
        exit(1)
    else:
        ROM_DIR = sys.argv[1]        
        GAMEDB_TXT_OVERWRITE = sys.argv[2]

    # ---
    rom_dir = ROM_DIR

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