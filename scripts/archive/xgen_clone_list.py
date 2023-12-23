import os
import json

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

rom_dir = EXTRACTED_CD_ROM_DIR

directories = [d for d in os.listdir(rom_dir) if os.path.isdir(os.path.join(rom_dir, d))] # rescan the dir again

    
# Cleaning up titles (removing newline characters)
game_titles = [title.strip() for title in directories]

# Creating the structure for each game title
clone_list = []

for title in game_titles:
    clone_item = {
        "group": title,
        "titles": [
            {"searchTerm": ""}
        ]
    }
    clone_list.append(clone_item)

# Writing the structure to a JSON file
with open('clonelist.json', 'w') as outfile:
    json.dump(clone_list, outfile, indent=4)
