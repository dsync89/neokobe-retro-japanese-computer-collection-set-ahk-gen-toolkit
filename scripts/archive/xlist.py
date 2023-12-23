import os
import zipfile
from collections import defaultdict

game_fd_only = []

game_titles_str = []


OUT_FOLDER = "s:\\_nec pc-98_out\\FD\\"

class GameTitles:
    def __init__(self):
        self.cd = []
        self.hd = []
        self.fd = []

def create_game_titles():
    return defaultdict(GameTitles)

def print_game_titles(game_titles):
    for game, titles_obj in game_titles.items():
        print(f"Game: {game}")
        print(f"CD Titles: {titles_obj.cd}")
        print(f"HDD Titles: {titles_obj.hd}")
        print(f"FDI Titles: {titles_obj.fd}")
        print()    

def print_list(prefix, list):
    print(prefix + ':')
    for _ in list:
        print("  " + _)

def find_zip_files_with_keywords(root_folder):
    zip_with_hd_cd = []  # List to store zip files containing [HD] and [CD]
    zip_only_fd = []  # List to store zip files containing only [FD]

    for root, dirs, files in os.walk(root_folder):
        # for directory in dirs[:]:  # Iterate over a copy of dirs to modify it safely
        #     if not directory.startswith('A'):
        #         dirs.remove(directory)  # Remove directories not starting with 'A'

        _fd = []
        _hd = []
        _cd = []

        print("---------------------------------------------------------------------")
        print("Dir: %s" % root)

        if len(files) > 0:
            game_titles_str.append(root)

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
                    print("oops, no FD, HD, or CD!, zip file: %s" % zip_path)

        game_titles[zip_path].cd = _cd
        game_titles[zip_path].fd = _fd
        game_titles[zip_path].hd = _hd

        # check _fd, _cd, and _hd array to see if
        if len(_cd) == 0 and len(_hd) == 0 and len(_fd) == 0:
            print("this folder has nothing!")
        elif len(_cd) == 0 and len(_hd) == 0 and len(_fd) > 0:
            print("this folder only has FD!")
            # game_fd_only.append(os.path.join(root))
            game_fd_only.append(zip_path)
        print_list('CD', _cd)
        print_list('HD', _hd)
        print_list('FD', _fd)

        print("next")


    return zip_with_hd_cd, zip_only_fd

def extract_zip_to_folder(zip_files, destination):
    for zip_file in zip_files:
        # Extract folder name from zip file path
        folder_name = os.path.splitext(os.path.basename(zip_file))[0]
        destination_path = os.path.join(destination, folder_name)
        
        # Create a folder with the same name as the zip file
        os.makedirs(destination_path, exist_ok=True)
        
        # Extract contents of the zip file to the created folder
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(destination_path)

# Example usage:
game_titles = create_game_titles()

root_folder_path = 's:\\_nec pc-98\\'
zip_with_hd_cd_files, zip_only_fd_files = find_zip_files_with_keywords(root_folder_path)

print("ZIP files containing [HD] and [CD]:")
print(zip_with_hd_cd_files)

print("\nZIP files containing only [FD]:")
print(zip_only_fd_files)

print("Found %d games with FD only" % len(game_fd_only))
print_list("Games with FD only", game_fd_only)

print_game_titles(game_titles);

# extract_zip_to_folder(game_fd_only, OUT_FOLDER)

# print("Total games: %d" % len(game_titles))
# print_list("Game Titles", game_titles)


