from pynput import keyboard


class KeyLogger:
    def __init__(self, filename: str = "log.txt"):
        self.filename = filename
        self._current_keys = set()
        

    # --- Keyboard functions ---
    def _on_press(self, key, injected = False):
        try:
            print(f"Keyboard: Key pressed -> {key.char}")
            
            if key.char == "\x16":
                print("Paste command")
            
        except AttributeError:
            print(f"Keyboard: Special key pressed -> {key}")




            
    def _on_release(self, key, injected = False):
        # Remove released key from set
        # try:
        #     self._current_keys.discard(key.char)
        # except AttributeError:
        #     self._current_keys.discard(key)

        print(f"Keyboard: Key released -> {key}")
        if key == keyboard.Key.esc:
            return False  # stop listener
        

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

