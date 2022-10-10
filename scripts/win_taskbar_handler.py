from ctypes import windll

h = windll.user32.FindWindowA(b'Shell_TrayWnd', None)  # get the handle to the taskbar


def hide():
    windll.user32.ShowWindow(h, 0)


def show():
    windll.user32.ShowWindow(h, 9)


if __name__ == '__main__':
    show()
