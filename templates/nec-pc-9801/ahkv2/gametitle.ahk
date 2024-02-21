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

					if InStr(_bootSource, ".2d") || InStr(_bootSource, ".d88") || InStr(_bootSource, ".hdm") || InStr(_bootSource, ".nfd") {
						FD := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34)
						fdArr.Push FD
					}   

					if InStr(_bootSource, ".hdi") {
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

				SplitPath destFilename, &name, &dir, &ext, &name_no_ext
				destFilename := dir "\" name_no_ext "-tmpzzz." ext

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
				
				SplitPath destFilename, &name, &dir, &ext, &name_no_ext
				destFilename := dir "\" name_no_ext "-tmpzzz." ext

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
				
				SplitPath destFilename, &name, &dir, &ext, &name_no_ext
				destFilename := dir "\" name_no_ext "-tmpzzz." ext

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

			IniPath := (emuDir . "\np21w.ini")	

			Loop fdArr.Length {
				if debug 
					MsgBox Format("Write INI: [NekoProject21] FDD{1}FILE={2}", A_Index, fdArr[A_Index])
				IniWrite fdArr[A_Index], IniPath, "NekoProject21", "FDD" . A_Index . "FILE"
			}

			Loop hdArr.Length {
				if debug 
					MsgBox Format("Write INI: [NekoProject21] HDD{1}FILE={2}", A_Index, hdArr[A_Index])
				IniWrite hdArr[A_Index], IniPath, "NekoProject21", "HDD" . A_Index . "FILE"
			}			

			Loop cdArr.Length {
				if debug 
					MsgBox Format("Write INI: [NekoProject21] CD{1}_FILE={2}", A_Index+2, cdArr[A_Index])
				IniWrite cdArr[A_Index], IniPath, "NekoProject21", "CD" . A_Index+2 . "_FILE"
			}	
			
			Loop ctArr.Length {
				; if debug 
				; 	MsgBox Format("Write INI: [RecentFiles] RecentTapePath1_{1}={2}", A_Index, ctArr[A_Index])
				; IniWrite ctArr[A_Index], IniPath, "RecentFiles", "RecentTapePath1_" . A_Index
			}						

			; =============================================================================================			
			bootArgs := ""
			If fdArr.Length > 0 {
				Loop fdArr.Length {
					bootArgs .= fdArr[A_Index] . " " ; Concatenate
				}
			}
			Else If ctArr.Length > 0
				bootArgs .= ctArr[1]
			
			If (startFullScreen == 1)
				bootArgs .= " /f "

			Command := emuPath " " bootArgs " /i " IniPath 
			If debug
				MsgBox Format("Command: {1}", Command)
			Run(Command)
			
		}    
	}
}

; ============================================================
; Key Bindings
; ============================================================

Esc::
{
	If (A_PriorHotkey = "Esc" and A_TimeSincePriorHotkey < 500) {
		ProcessClose "np21w.exe"
		Run "taskkill /im np21w.exe /F",, "Hide"
		ExitApp
	}
}