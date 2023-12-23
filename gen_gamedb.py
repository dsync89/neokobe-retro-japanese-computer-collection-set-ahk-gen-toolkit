# generate a .gamedb.txt file that list all the files in each game folder as a row in the format of
# GAMETITLE | FILE 1 | FILE 2 | FILE 3 ...

import os
import sys
import json

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
if __name__ == "__main__":

    if len(sys.argv) != 2:
        print("Usage: python script.py <ROM_DIR>")
        exit(1)
    else:
        arg1 = sys.argv[1]        
        ROM_DIR = arg1

    root_folder_path = ROM_DIR
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
