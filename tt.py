import win32gui


def get_all_windows():
    windows = []

    def enum_windows_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            window_title = win32gui.GetWindowText(hwnd)
            windows.append((hwnd, window_title))

    win32gui.EnumWindows(enum_windows_callback, None)

    return windows

# Example usage
all_windows = get_all_windows()
for hwnd, title in all_windows:
    print(f"Window Handle: {hwnd}\tTitle: {title}")
