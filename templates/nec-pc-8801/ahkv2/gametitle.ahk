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

root := romDir

CCD := ""
HDI := ""
FDD := ""

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

		;MsgBox GameInfo[1]
		;MsgBox scriptFileName

		; Check if the AHK script's filename matches the GameTitle
		if (gameTitle = scriptFileName)
		{
			; MsgBox Format("Found matching game title in gamedb, title: {1}", gameTitle)
			; MsgBox Format("Found {1} files", elementCount)

			FDDS := "" ; store the concatenated bootsources

			fddArr := Array()

			Loop(GameInfo.Length) {
				if (A_Index > 1)
				{
					_bootSource := Trim(GameInfo[A_Index])
					; MsgBox, boot source %A_Index% is %_bootSource%					

					; check if this is a .hdm
					if InStr(_bootSource, ".2d") || InStr(_bootSource, ".d88") || InStr(_bootSource, ".hdm") {
						; MsgBox, The string contains '.hdm'.
						FDD := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34)
						fddArr.Push FDD
						FDDS .= FDD . " " ; Concatenate
					}   

					if InStr(_bootSource, ".hdi") {
						; MsgBox, The string contains '.hdi'.
						HDI := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34) . " "
					}      

					if InStr(_bootSource, ".ccd") {
						; MsgBox, The string contains '.ccd'.
						CCD := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34) . " "
					}                        

				}
			}

			; Trim any trailing white space for the concatenated boot source
			FDDS := Trim(FDDS)

			; MsgBox Format("HDI: {1}, CCD: {2}, FDDS: {3}", HDI, CCD, FDDS)

			; =============================================================================================
			; Write path to ini file because emu doesn't support argument to pass additional FDD file
			; =============================================================================================
			SplitPath emuPath, &emuFileName, &emuDir

			IniPath := (emuDir . "\pc8801ma_lb.ini")

			OrigIniPath := (emuDir . "\pc8801ma.ini")
			
			If FileExist(IniPath)
				FileDelete(IniPath) 
			
			Ini := FileRead(OrigIniPath)
			TmpIni := FileOpen(IniPath, "rw")
			
			; MsgBox Format("FD1: {1}, FD2: {2}", fddArr[1], fddArr[2])			

			Loop parse, Ini, "`n", "`r" {
				If InStr(A_LoopField, "RecentDiskPath1_1")
					TmpIni.WriteLine("RecentDiskPath1_1=" . fddArr[1])  
				Else If InStr(A_LoopField, "RecentDiskPath2_1")
					If fddArr.Length > 1
						TmpIni.WriteLine("RecentDiskPath2_1=" . fddArr[2])
					Else
						TmpIni.WriteLine("RecentDiskPath2_1=" . " ")                                       
				Else If (A_LoopField = "")
					Continue
				Else
					TmpIni.WriteLine(A_LoopField)
			}
			TmpIni.Close()

			FileCopy IniPath, OrigIniPath, 1 ; Overwrite orig ini if exist
			; =============================================================================================			
		
			; Prompt user to select Disk2 from menu if FD more than 1
			If fddArr.Length > 1
				MsgBox "Select FD2 from menu because this game has more than 1 FD"

			Run(emuPath " " fddArr[1]) ; 

			; Start in full screen if the game only has 1 FD and config startFullScreen=1
			If (startFullScreen == 1 and fddArr.Length == 1) {
				; Start in full screen since the emu doesn't have full screen startup argument
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