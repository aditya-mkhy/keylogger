from datetime import datetime
import win32gui
import win32process
import psutil
from pathlib import Path
import os

def get_time():
    return datetime.now().strftime("%d-%m-%Y %H:%M:%S")


def get_active_window() -> dict:
    hwnd = win32gui.GetForegroundWindow()  # Get handle of active window
    pid = win32process.GetWindowThreadProcessId(hwnd)[1]  # Get process ID
    process = psutil.Process(pid)  # Get process info

    window_title = win32gui.GetWindowText(hwnd)
    exe_name = process.name()

    return {"title": window_title, "exe": exe_name}


def get_save_info(win_info: dict = None) -> str:
    if not win_info:
        win_info = get_active_window()

    return f"{get_time()} [{win_info['exe']} --> {win_info['title']}]"


def log(*args, **kwargs):
    # print(*args, **kwargs)
    return

def get_save_dirname():
    path = f"{Path.home()}\\.window\\info"
    os.makedirs(path, exist_ok=True)
    if os.path.exists(path):
        return path
    

def get_num_from_text(text: str):
    num = ""
    is_digit = False

    for ch in text:
        if ch.isdigit():
            if not is_digit:
                is_digit = True
            num += ch
            continue

        if is_digit:
            try:
                return int(num)
            except:
                return 0

def get_filename(max_size = 100):
    
    files = os.listdir(get_save_dirname())
    if len(files) == 0:
        return os.path.join(get_save_dirname(), "log1.txt")
    
    files.sort(reverse=True)
    to_use_file = files[0]
    full_path = os.path.join(get_save_dirname(), to_use_file)

    if os.path.getsize(full_path) < max_size:
        return full_path
    
    num = get_num_from_text(to_use_file)
    new_filename = f"log{num + 1}.txt"
    return os.path.join(get_save_dirname(), new_filename)
    
    




if __name__ == "__main__":
    print(get_filename())