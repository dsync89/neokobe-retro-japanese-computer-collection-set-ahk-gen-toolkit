; Get the full path of the script
scriptFullPath := A_ScriptFullPath
scriptDirectory := StrReplace(scriptFullPath, A_ScriptName, "")
scriptFileName := SubStr(A_ScriptName, 1, StrLen(A_ScriptName) - 4) ; Remove ".ahk" extension

; Read the config.txt file
configFile := A_ScriptDir . "\" . ".config.ini"

; Read values from the config.txt file
emuPath := IniRead(configFile, "Settings", "EmuPath")
gameDbPath := IniRead(configFile, "Settings", "GameDbPath")
fdRomDir := IniRead(configFile, "RomPath", "FDRomDir")
hdRomDir := IniRead(configFile, "RomPath", "HDRomDir")
cdRomDir := IniRead(configFile, "RomPath", "CDRomDir")

;MsgBox(LTrim
;    "Emu Path: " emuPath "`n"
;    "GameDB Path: " gameDbPath "`n"
;    "FD ROM Dir: " fdRomDir "`n"
;    "HD ROM Dir: " hdRomDir "`n"
;    "CD ROM Dir: " cdRomDir
;)

root := cdRomDir

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

			; =============================================================================================
			; Write HDD1FILE var to ini file because np21w doesn't support argument to pass HDD file path
			; =============================================================================================
			SplitPath emuPath, &emuFileName, &emuDir

			; IniPath := emuDir . "\np2
			IniPath := (emuDir . "\np21w_lb.ini")

			OrigIniPath := (emuDir . "\np21w.ini")
			
			If FileExist(IniPath)
				FileDelete(IniPath) 
			
			Ini := FileRead(OrigIniPath)
			TmpIni := FileOpen(IniPath, "rw")                
					
			Loop parse Ini, "`n`,`r" {
				If InStr(A_LoopField, "HDD1FILE")
					TmpIni.WriteLine("HDD1FILE=" . HDI)  
				Else If InStr(A_LoopField, "FDD1FILE")
					TmpIni.WriteLine("FDD1FILE=")
				Else If InStr(A_LoopField, "FD1NAME0")
					TmpIni.WriteLine("FD1NAME0=") 
				Else If InStr(A_LoopField, "CD3_FILE")
					TmpIni.WriteLine("CD3_FILE=" . CCD)                                        
				Else If (A_LoopField = "")
					Continue
				Else
					TmpIni.WriteLine(A_LoopField)
			}
			TmpIni.Close()
			; =============================================================================================

			RunWait(emuPath " /f /i " IniPath " " FDDS) ; Start emu in full screen and pass the modified ini path with HDD1FILE path 

			FileDelete(IniPath)        
		}    
	}
}

; ============================================================
; Key Bindings
; ============================================================

Esc::
{
    ProcessClose "np21w.exe"
    Run "taskkill /im np21w.exe /F",, "Hide"
    FileDelete(IniPath)  
    ExitApp
}