@echo off
python3 .\gen_gamedb.py
python3 .\gen_gamedb_with_overrides.py
python3 .\gen_ahk_files.py
python3 .\add_keymapper_to_ahk.py