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

			Loop(GameInfo.Length) {
				if (A_Index > 1)
				{
					_bootSource := Trim(GameInfo[A_Index])
					; MsgBox, boot source %A_Index% is %_bootSource%					

					; check if this is a .hdm
					if InStr(_bootSource, ".d88") || InStr(_bootSource, ".hdm") {
						; MsgBox, The string contains '.hdm'.
						FDD := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34) . " "
					}   

					if InStr(_bootSource, ".hdi") {
						; MsgBox, The string contains '.hdi'.
						HDI := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34) . " "
					}      

					if InStr(_bootSource, ".ccd") {
						; MsgBox, The string contains '.ccd'.
						CCD := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34) . " "
					}                        

					FDDS .= FDD . " " ; Concatenate
				}
			}    

			; MsgBox Format("HDI: {1}, CCD: {2}, FDDS: {3}", HDI, CCD, FDDS)
		
			Run(emuPath " " FDDS) ; 

			; Start in full screen since the emu doesn't have full screen startup argument
			Sleep 1000 ; Give some time for the emulator to start
			Send "{Alt Down}" ; Press and hold ALT
			Send "{Enter}" ; Press ENTER
			Send "{Alt Up}" ; Release ALT

		}    
	}
}

; ============================================================
; Key Bindings
; ============================================================

Esc::
{
    ProcessClose "xm6g.exe"
    Run "taskkill /im xm6g.exe /F",, "Hide"
    ExitApp
}