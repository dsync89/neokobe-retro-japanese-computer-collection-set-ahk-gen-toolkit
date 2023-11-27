import os
import zipfile
from collections import defaultdict
import json
import shutil

# Set whether you want to extract all zip found for a game folder, or the last one found only
# if set to True, this will only add the last zip file found in a game folder,
#
# e.g. if a folder contains:
# 1. Xak III - The Eternal Recurrence [FD] [Set 1].zip
# 2. Xak III - The Eternal Recurrence [FD].zip
#
# It will only extract Xak III - The Eternal Recurrence [FD].zip 
is_add_last_zip_only = True # only add the last zip found per game title

# Read the configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)

ROM_DIR = config.get('rom_dir') # the extracted neokobe zip files
EXTRACTED_FD_ROM_DIR = config.get('extracted_fd_rom_dir')
EXTRACTED_HD_ROM_DIR = config.get('extracted_hd_rom_dir')
EXTRACTED_CD_ROM_DIR = config.get('extracted_cd_rom_dir')

# create extracted folder path if not exist
os.makedirs(EXTRACTED_FD_ROM_DIR, exist_ok=True)
os.makedirs(EXTRACTED_HD_ROM_DIR, exist_ok=True)
os.makedirs(EXTRACTED_CD_ROM_DIR, exist_ok=True)

# -----------------------------------------------------------
# DO NOT MODIFY
# -----------------------------------------------------------

class GameTitles:
    def __init__(self):
        self.cd = []
        self.hd = []
        self.fd = []

def create_game_titles():
    return defaultdict(GameTitles)

def filter_game_titles(game_titles, filter, is_add_last_zip_only):
    zip_files = []

    for game, media_type in game_titles.items():
        gameTitle = os.path.basename(os.path.normpath(game))

        print("Processing game...")
        print(f"Game Path: {game}")
        print(f"Game Title: {gameTitle}")
        print(f"CD Titles: {media_type.cd}")
        print(f"HD Titles: {media_type.hd}")
        print(f"FD Titles: {media_type.fd}")

        if filter.lower() == 'fd':
            if len(media_type.cd) == 0 and len(media_type.hd) == 0 and len(media_type.fd) > 0:
                print("Media Type identified as: FD")

                if is_add_last_zip_only == True:
                    for index, item in enumerate(media_type.fd):
                        if index == len(media_type.fd) - 1:  # Check if it's the last element
                            zip_files.append(item)
                else:
                    for item in media_type.fd:
                        zip_files.append(item)
            
        elif filter.lower() == 'hd':
            if len(media_type.cd) == 0 and len(media_type.hd) > 0 and len(media_type.fd) > 0:
                print("Media Type identified as: HD")

                if is_add_last_zip_only == True:
                    for index, item in enumerate(media_type.hd):
                        if index == len(media_type.hd) - 1:  # Check if it's the last element
                            zip_files.append(item)
                else:
                    for item in media_type.hd:
                        zip_files.append(item)

        elif filter.lower() == 'cd':
            if len(media_type.cd) > 0 and len(media_type.hd) >= 0 and len(media_type.fd) >= 0:
                print("Media Type identified as: CD")

                if is_add_last_zip_only == True:
                    for index, item in enumerate(media_type.cd):
                        if index == len(media_type.cd) - 1:  # Check if it's the last element
                            zip_files.append(item)
                else:
                    for item in media_type.cd:
                        zip_files.append(item)
                    for item in media_type.hd: # also add HD zip file because some might contain (CD version)
                        if 'FD version' in item: # don't include with FD version, we just want CD version
                            continue       
                        zip_files.append(item)
                    for item in media_type.fd: 
                        if gameTitle in ('Policenauts'): # manually add game here
                            zip_files.append(item)     

        print()

    return zip_files

def print_game_titles(game_titles):
    for game, titles_obj in game_titles.items():
        print(f"Game: {game}")
        print(f"CD Titles: {titles_obj.cd}")
        print(f"HDD Titles: {titles_obj.hd}")
        print(f"FDI Titles: {titles_obj.fd}")
        print()    

def print_game_titles_stats(game_titles):
    numMediaTypeFd = 0
    numMediaTypeHd = 0
    numMediaTypeCd = 0
    numMediaTypeUnknown = 0

    for game, media_type in game_titles.items():
        if len(media_type.cd) == 0 and len(media_type.hd) == 0 and len(media_type.fd) > 0:
            numMediaTypeFd = numMediaTypeFd+1
        elif len(media_type.cd) == 0 and len(media_type.hd) > 0 and len(media_type.fd) > 0:
            numMediaTypeHd = numMediaTypeHd+1
        elif len(media_type.cd) > 0 and len(media_type.hd) >= 0 and len(media_type.fd) >= 0:
            numMediaTypeCd = numMediaTypeCd+1
        else:
            numMediaTypeUnknown = numMediaTypeUnknown+1
    
    print("Games with FD only: {}".format(numMediaTypeFd))
    print("Games with HD: {}".format(numMediaTypeHd))
    print("Games with CD: {}".format(numMediaTypeCd))
    print("Games with Unknown Media Types (probably Extra files): {}".format(numMediaTypeUnknown))

def print_list(prefix, list):
    print(prefix + ':')
    for _ in list:
        print("  " + _)

def populate_game_titles(root_folder):
    zip_with_hd_cd = []  # List to store zip files containing [HD] and [CD]
    zip_only_fd = []  # List to store zip files containing only [FD]

    for root, dirs, files in os.walk(root_folder):

        _fd = []
        _hd = []
        _cd = []

        print("---------------------------------------------------------------------")
        print("Dir: %s" % root)


        if len(files) == 0:
            continue

        for file in files:
            if file.endswith('.zip'):
                zip_path = os.path.join(root, file)
          
                has_hd = '[HD' in file.upper()
                has_cd = '[CD' in file.upper()
                has_fd = '[FD' in file.upper()

                if has_fd:
                    _fd.append(zip_path)
                elif has_cd:
                    _cd.append(zip_path)
                elif has_hd:
                    _hd.append(zip_path)
                else:
                    print("oops, this zip file is is NOT FD, HD, or CD media type, ignoring it: %s" % zip_path)

        game_titles[root].cd = _cd
        game_titles[root].fd = _fd
        game_titles[root].hd = _hd

        print_list('CD', _cd)
        print_list('HD', _hd)
        print_list('FD', _fd)       

def extract_zip_to_folder(zip_files, destination):
    for index, zip_file in enumerate(zip_files):    
        # Extract folder name from zip file path
        folder_name = os.path.splitext(os.path.basename(zip_file))[0]

        destination_path = os.path.join(destination, folder_name)
        
        # Create a folder with the same name as the zip file
        os.makedirs(destination_path, exist_ok=True)
        
        # Extract contents of the zip file to the created folder
        print("Extracting [{}/{}] zip file: {} ==> {}".format(index+1, len(zip_files), zip_file, destination_path))

        try:
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(destination_path)
        except:
            print("ops")
            continue

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------

if __name__ == "__main__":
    game_titles = create_game_titles()

    populate_game_titles(ROM_DIR)

    print()
    # print_game_titles(game_titles);
    print("Found %d total games" % len(game_titles))
    print()

    print_game_titles_stats(game_titles)

    print()

    media_type = ''
    media_type_choices = ['cd', 'fd', 'hd']

    extracted_dir = ''
    is_add_last_zip_only = False

    print()
    user_input = input("Please enter a a media type to extract [fd, hd, cd]: ")
    if any(media_type in user_input for media_type in media_type_choices):
        for media_type in media_type_choices:
            if media_type in user_input:
                print("Selection: {}".format(media_type))
                media_type = user_input

                if media_type == 'cd':
                    extracted_dir = EXTRACTED_CD_ROM_DIR
                    is_add_last_zip_only = False
                elif media_type == 'hd':
                    extracted_dir = EXTRACTED_HD_ROM_DIR
                    is_add_last_zip_only = True
                elif media_type == 'fd':
                    extracted_dir = EXTRACTED_FD_ROM_DIR
                    is_add_last_zip_only = True

                break

    if len(media_type) == 0:
        print("Invalid choice!")
        exit(1)

    zip_files = filter_game_titles(game_titles, media_type, is_add_last_zip_only)
    print_list("Game List: ", zip_files)    
    print("Found %d zip files to extract" % len(zip_files))

    print()
    user_input = input("Enter Y/y to start extracting: ")
    if user_input == 'y' or user_input == 'Y':
        print("Extracting {} games to {}".format(len(zip_files), extracted_dir))
        extract_zip_to_folder(zip_files, extracted_dir)
    else:
        print('bye!')
        