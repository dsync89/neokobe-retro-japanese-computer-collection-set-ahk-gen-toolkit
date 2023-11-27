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

; MsgBox, 
; (LTrim
;    Emu Path: %emuPath%
;    GameDB Path: %gameDbPath%
;    FD ROM Dir: %fdRomDir%
;    HD ROM Dir: %hdRomDir%
;    CD ROM Dir: %cdRomDir%
; )

root := fdRomDir

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

        FDD := ""

        Loop, %GameInfo0%
        {
            if (A_Index > 1)
            {
                _bootSource := Trim(GameInfo%A_Index%)

                if InStr(_bootSource, ".hdm") || InStr(_bootSource, ".d88") || InStr(_bootSource, ".nfd")
                    FDD := Chr(34) . root . "\" . gameTitle . "\" . _bootSource . Chr(34) . " "

                FDDS .= FDD . " " ; Concatenate
            }
        }    

        ; MsgBox, Full command %FDDS%

        RunWait, %emuPath% /f %FDDS%
    }    



}

; ==============================
; Key Bindings
; ==============================

Esc::
    Process, Close, np21w.exe
    Run, taskkill /im np21w.exe /F,, Hide
    FileDelete, %IniPath%  
    ExitApp