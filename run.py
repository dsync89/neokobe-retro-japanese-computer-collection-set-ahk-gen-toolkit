import json
import subprocess

def run_gen_gamedb_py(rom_dir):    
    script_path = 'gen_gamedb.py'
    try:
        subprocess.run(["python3", script_path, rom_dir])
    except FileNotFoundError:
        print(f"File '{script_path}' not found.")  

def run_gen_gamedb_with_overrides_py(rom_dir, gamedb_overwrite_file):    
    script_path = 'gen_gamedb_with_overrides.py'
    try:
        subprocess.run(["python3", script_path, rom_dir, gamedb_overwrite_file])
    except FileNotFoundError:
        print(f"File '{script_path}' not found.")        

def run_gen_ahk_files_py(rom_dir, template_dir, gametitle_dir):   
    script_path = 'gen_ahk_files.py' 
    try:
        subprocess.run(["python3", script_path, rom_dir, template_dir, gametitle_dir])
    except FileNotFoundError:
        print(f"File '{script_path}' not found.")  
  
def run_add_keymapper_to_ahk_py(rom_dir, keymap_dir):   
    script_path = 'add_keymapper_to_ahk.py' 
    try:
        subprocess.run(["python3", script_path, rom_dir, keymap_dir])
    except FileNotFoundError:
        print(f"File '{script_path}' not found.") 

# -----------------------------------------------------------
# Main
# -----------------------------------------------------------
if __name__ == "__main__":

    # Read JSON data from the file
    with open('.\config.json', 'r') as file:
        json_data = json.load(file)

    # Iterate through each element in "platforms"
    for set in json_data['sets']:
        print("Platform: ", set['platform'])
        print("Enable: ", set["enable"])
        rom_dir = set['config']['rom_dir']
        template_dir = set['config']['template_dir']
        keymap_dir = set['config']['keymap_dir']
        gametitle_dir = set['config']['gametitle_dir']
        gamedb_overwrite_file = set['config']['gamedb_overwrite_file']
        print("ROM Dir: ", rom_dir)
        print("Template Dir: ", template_dir)
        print("Keymap Dir: ", keymap_dir)
        print("Game Title Dir: ", gametitle_dir)
        print("GameDb Overwrite File: ", gamedb_overwrite_file)
        print("-------------------")

        if set["enable"]:
            run_gen_gamedb_py(rom_dir)
            run_gen_gamedb_with_overrides_py(rom_dir, gamedb_overwrite_file)
            run_gen_ahk_files_py(rom_dir, template_dir, gametitle_dir)     
            run_add_keymapper_to_ahk_py(rom_dir, keymap_dir)              