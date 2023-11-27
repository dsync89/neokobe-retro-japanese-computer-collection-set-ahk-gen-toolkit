; Get the full path of the script
scriptFullPath := A_ScriptFullPath
scriptDirectory := StrReplace(scriptPath, A_ScriptName, "")
scriptFileName := SubStr(A_ScriptName, 1, StrLen(A_ScriptName) - 4) ; Remove ".ahk" extension

; Read the config.txt file
configFile := A_ScriptDir . "\" . ".config.ini"

; Read values from the config.txt file
IniRead, emuPath, %configFile%, Settings, EmuPath
IniRead, gameDbPath, %configFile%, Settings, GameDbPath
IniRead, fdRomDir, %configFile%, RomPath, FDRomDir
IniRead, hdRomDir, %configFile%, RomPath, HDRomDir
IniRead, cdRomDir, %configFile%, RomPath, CDRomDir

;MsgBox, 
;(LTrim
;    Emu Path: %emuPath%
;    GameDB Path: %gameDbPath%
;    FD ROM Dir: %fdRomDir%
;    HD ROM Dir: %hdRomDir%
;    CD ROM Dir: %cdRomDir%
;)

root := hdRomDir

CCD := ""
HDI := ""
FDD := ""

; Read each line in the game until a match is found
Loop, read, %gameDbPath%
{
    LineText := A_LoopReadLine
    if LineText =
        break

    ; Split the line into parts using |
    StringSplit, GameInfo, LineText, `|

    ; Get the number of elements after splitting
    elementCount := GameInfo0

    gameTitle := Trim(GameInfo1)

    ; MsgBox, GameTitle: %GameTitle% , ScriptFileName: %scriptFileName%

    ; Check if the AHK script's filename matches the GameTitle
    if (gameTitle = scriptFileName)
    {
        MsgBox, Found matching game title in gamedb, title: %GameTitle%
        ; MsgBox, "Found files: " . %elementCount%

        FDDS := "" ; store the concatenated bootsources

        Loop, %GameInfo0%
        {
            if (A_Index > 1)
            {
                _bootSource := Trim(GameInfo%A_Index%)
                ; MsgBox, boot source %A_Index% is %_bootSource%

                ; check if this is a .hdm
                if InStr(_bootSource, ".hdm") {
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

        ; MsgBox, Full command %bootSources%

        ; =============================================================================================
        ; Write HDD1FILE var to ini file because np21w doesn't support argument to pass HDD file path
        ; =============================================================================================
        SplitPath, emuPath, , emuDir, ,

        IniPath := emuDir . "\np21w_lb.ini"
        OrigIniPath := emuDir . "\np21w.ini"

        If FileExist(IniPath)
            FileDelete, %IniPath% 
        
        FileRead, Ini, %OrigIniPath%
        TmpIni := FileOpen(IniPath, "w")                
                
        Loop, parse, Ini, `n, `r 
        {
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

        RunWait, %emuPath% /f /i %IniPath% %FDD% ; Start emu in full screen and pass the modified ini path with HDD1FILE path 

        FileDelete, %IniPath%        
    }    
}

; ============================================================
; Key Bindings
; ============================================================

Esc::
    Process, Close, np21w.exe
    Run, taskkill /im np21w.exe /F,, Hide
    FileDelete, %IniPath%  
    ExitApp

; ============================================================
; Key Bindings imported from keymapping\hd\global.ahk
; ============================================================
Up::Numpad8
Down::Numpad2
Left::Numpad4
Right::Numpad6

; ============================================================
; Key Bindings imported from keymapping\hd\Rusty.ahk
; ============================================================
Ctrl::z
Alt::x