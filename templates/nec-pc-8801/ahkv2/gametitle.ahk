; Get the full path of the script
scriptFullPath := A_ScriptFullPath
scriptDirectory := StrReplace(scriptFullPath, A_ScriptName, "")
scriptFileName := SubStr(A_ScriptName, 1, StrLen(A_ScriptName) - 4) ; Remove ".ahk" extension

; Read the config.txt file
configFile := A_ScriptDir . "\" . ".config.ini"

; Read values from the config.txt file
emuPath := IniRead(configFile, "Settings", "EmuPath")
gameDbPath := IniRead(configFile, "Settings", "GameDbPath")
romDir := IniRead(configFile, "RomPath", "RomDir")
startFullScreen := IniRead(configFile, "Settings", "StartFullScreen")
debug := IniRead(configFile, "Settings", "Debug")

root := romDir

CT := ""
CD := ""
HD := ""
FD := ""

; Read each line in the game until a match is found
Contents := FileRead(gameDbPath)  ; Read the entire file into 'Contents' variable

Loop Read gameDbPath `n  ; Loop through each line (assuming newline as delimiter)
{
	Loop parse, A_LoopReadLine, A_Tab
	{
		LineText := A_LoopField
		if LineText = ""
			break

		; Split the line into parts using |
		GameInfo := StrSplit(LineText, "|")

		; Get the number of elements after splitting
		elementCount := GameInfo.Length

		gameTitle := Trim(GameInfo[1])

		; Check if the AHK script's filename matches the GameTitle
		if (gameTitle = scriptFileName)
		{
			ctArr := Array()
			fdArr := Array()
			hdArr := Array()
			cdArr := Array()

			bootNotes := ""

			Loop(GameInfo.Length) {
				if (A_Index > 1)
				{
					_bootSource := Trim(GameInfo[A_Index])					

					if InStr(_bootSource, ".2d") || InStr(_bootSource, ".d88") {
						FD := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34)
						fdArr.Push FD
					}   

					if InStr(_bootSource, ".hdf") {
						HD := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34)
						hdArr.Push HD
					}      

					if InStr(_bootSource, ".ccd") {
						CD := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34)
						cdArr.Push CD
					}

					if InStr(_bootSource, ".t88") || InStr(_bootSource, ".tap") {
						CT := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34)
						ctArr.Push CT
					}  					

					if InStr(_bootSource, "Notes:") {
						bootNotes := _bootSource
					} 					
				}
			}    

			; Print detected boot media
			Loop fdArr.Length {
				if debug 
					MsgBox Format("FD{1}: {2}", A_Index-1, fdArr[A_Index])
			}
			Loop hdArr.Length {
				if debug 
					MsgBox Format("HD{1}: {2}", A_Index-1, hdArr[A_Index])
			}
			Loop cdArr.Length {
				if debug 
					MsgBox Format("CD{1}: {2}", A_Index-1, cdArr[A_Index])
			}
			Loop ctArr.Length {
				if debug 
					MsgBox Format("CT{1}: {2}", A_Index-1, ctArr[A_Index])
			}		
			
			; =============================================================================================
			; Make a copy of the original rom file for loading to emulator later so that emulator won't
			; modify any original rom file for DAT sake!
			; =============================================================================================			
			Loop fdArr.Length {
				srcFilename := fdArr[A_Index]
				destFilename := srcFilename
				srcFilename := StrReplace(srcFilename, Chr(34), "")
				destFilename := StrReplace(destFilename, Chr(34), "")				
				destFilename .= "-tmpzzz.hdi"

				if debug
					MsgBox Format("srcFilename={1}, destFilename={2}", srcFilename, destFilename)
				if not FileExist(destFilename)
					FileCopy srcFilename, destFilename

				; remove Read-only attrib
				FileSetAttrib "-R", destFilename

				fdArr[A_Index] := Chr(34) destFilename Chr(34)
				if debug
					MsgBox Format("new fdArr[{1}]={2}", A_Index, fdArr[A_Index])
			}

			Loop hdArr.Length {
				srcFilename := hdArr[A_Index]
				destFilename := srcFilename
				srcFilename := StrReplace(srcFilename, Chr(34), "")
				destFilename := StrReplace(destFilename, Chr(34), "")				
				destFilename .= "-tmpzzz.hdi"

				if debug
					MsgBox Format("srcFilename={1}, destFilename={2}", srcFilename, destFilename)
				if not FileExist(destFilename)
					FileCopy srcFilename, destFilename

				; remove Read-only attrib
				FileSetAttrib "-R", destFilename

				hdArr[A_Index] := Chr(34) destFilename Chr(34)
				if debug
					MsgBox Format("new hdArr[{1}]={2}", A_Index, hdArr[A_Index])
			}

			Loop ctArr.Length {
				srcFilename := ctArr[A_Index]
				destFilename := srcFilename
				srcFilename := StrReplace(srcFilename, Chr(34), "")
				destFilename := StrReplace(destFilename, Chr(34), "")				
				destFilename .= "-tmpzzz.hdi"

				if debug
					MsgBox Format("srcFilename={1}, destFilename={2}", srcFilename, destFilename)
				if not FileExist(destFilename)
					FileCopy srcFilename, destFilename

				; remove Read-only attrib
				FileSetAttrib "-R", destFilename

				ctArr[A_Index] := Chr(34) destFilename Chr(34)
				if debug
					MsgBox Format("new ctArr[{1}]={2}", A_Index, ctArr[A_Index])
			}				
		
			; =============================================================================================
			; Modify ini file because emu doesn't support argument to pass additional media files
			; =============================================================================================
			SplitPath emuPath, &emuFileName, &emuDir

			IniPath := (emuDir . "\pc8801ma.ini")	

			Loop fdArr.Length {
				if debug 
					MsgBox Format("Write INI: [RecentFiles] RecentDiskPath{1}_1={2}", A_Index, fdArr[A_Index])
				IniWrite fdArr[A_Index], IniPath, "RecentFiles", "RecentDiskPath" . A_Index . "_1"
			}

			Loop hdArr.Length {
				if debug 
					MsgBox Format("Write INI: [RecentFiles] RecentHardDiskPath{1}_1={2}", A_Index, fdArr[A_Index])
				IniWrite fdArr[A_Index], IniPath, "RecentFiles", "RecentHardDiskPath" . A_Index . "_1"
			}			

			Loop cdArr.Length {
				; if debug
				;	MsgBox Format("Write INI: [MRU3] File0={1}", cdArr[A_Index])
				; IniWrite cdArr[A_Index], IniPath, "MRU3", "File0"
			}	
			
			Loop ctArr.Length {
				if debug 
					MsgBox Format("Write INI: [RecentFiles] RecentTapePath1_{1}={2}", A_Index, ctArr[A_Index])
				IniWrite ctArr[A_Index], IniPath, "RecentFiles", "RecentTapePath1_" . A_Index
			}			

			; Prompting user to manually click FDD1 and select 2nd FD if more than 1 FD disks is found
			if fdArr.Length > 1 {
				If StrLen(bootNotes) > 0 ; print the custom message in gamedb overwrite for more complex instructions
					MsgBox Format("{1}", bootNotes)
				Else
					MsgBox "Select the first item from [Menu > FD1] because this game require it to boot"
			}

			else if ctArr.Length > 0 {
				If StrLen(bootNotes) > 0 ; print the custom message in gamedb overwrite for more complex instructions
					MsgBox Format("{1}", bootNotes)
				Else
					MsgBox "Select the first item from [Menu > CMT] because this game require it to boot. Note: You might hear some static cracking noise, please wait and the game should load..."
			}

			; =============================================================================================			
			If fdArr.Length == 0
				Run(emuPath)
			Else If fdArr.Length > 0
				Run(emuPath " " fdArr[1])
			Else If ctArr.Length > 0
				Run(emuPath " " ctArr[1])

			; Start in full screen if the game only has 1 FD and config startFullScreen=1
			If (startFullScreen == 1) {
				Sleep 1000 ; Give some time for the emulator to start
				Send "{Alt Down}" ; Press and hold ALT
				Send "{Enter}" ; Press ENTER
				Send "{Alt Up}" ; Release ALT
			}
		}    
	}
}

; ============================================================
; Key Bindings
; ============================================================

Esc::
{
    ProcessClose "pc8801ma.exe"
    Run "taskkill /im pc8801ma.exe /F",, "Hide"
    ExitApp
}