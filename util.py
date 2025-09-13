from datetime import datetime
import win32gui
import win32process
import psutil

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
    print(*args, **kwargs)
    return

if __name__ == "__main__":
    print(get_save_info())