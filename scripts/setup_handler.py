import win32ui
import win32gui
import win32con
import pyautogui
import webbrowser
from time import sleep
from os import startfile
from scripts.pysin import locate, wait_for, read_number, wait_for_multiple
from scripts.utils import rtime


def get_chrome_hwnd() -> 'int':
    result = []

    def winEnumHandler(hwnd, ctx):
        name_fragments = ['FUT', 'Web', 'App']
        condition = lambda x: True if all(frag in win32gui.GetWindowText(hwnd) for frag in name_fragments) else False
        if win32gui.IsWindowVisible(hwnd) and condition(hwnd): result.append(hwnd)

    win32gui.EnumWindows(winEnumHandler, None)
    if result: return result[0]


def open_web_app():
    coords = {'x': 0, 'y': 0, 'xz': 2560 - 1, 'yz': 1440 - 1}
    hwnd = get_chrome_hwnd()
    if not hwnd:
        startfile(r'links\chrome.lnk')
        sleep(2)
        webbrowser.open(r'https://www.ea.com/de-de/fifa/ultimate-team/web-app/')
        print('waiting for website to build up, due to slow ea server ...')
        sleep(1)
        hwnd = get_chrome_hwnd()
    window = pyautogui.Window(hwnd)
    if window.isMinimized:
        window.maximize()
    window.moveTo(coords['x'], coords['y'])
    window.resizeTo(coords['xz'], coords['yz'])
    win_window = win32ui.CreateWindowFromHandle(hwnd)
    win_window.SetForegroundWindow()
    pyautogui.hotkey('ctrl', '0')
    rtime()
    pyautogui.press('pgup')
    sleep(4)
    # open_first_tab = 'ctrl', '1'
    # pyautogui.press(*open_first_tab)
    # close_first_tab = 'ctrl', 'w'
    # pyautogui.press(*close_first_tab)


def get_fut_stats(trading_number_storage_handle):
    zoom_in()
    big_num = read_number(size='big_num', reg=(638, 863, 852 - 638, 1035 - 863))
    small1 = read_number(size='small_num', reg=(1295, 898, 1464 - 1295, 997 - 898))
    small2 = read_number(size='small_num', reg=(1217, 1030, 1433 - 1217, 1130 - 1030))
    tiny = read_number(size='tiny_num', reg=(1726, 320, 2226 - 1726, 402 - 320))
    if small1:
        trading_number_storage_handle.set_succ_purchase(small1)
    pyautogui.hotkey('ctrl', '0')
    return big_num, small1, small2, tiny


def zoom_in():
    pyautogui.hotkey('ctrl', '0')
    rtime()
    main_menu = wait_for(r'pics/nav_main_on.png', reg=(9, 194, 131 - 9, 280 - 194), sleep_dur=.1, max_iterations=30)
    if not main_menu:
        main_menu_deselected = locate(r'pics/nav_main_off.png', reg=(9, 194, 131 - 9, 280 - 194))
        if main_menu_deselected:
            pyautogui.click(main_menu_deselected)
            rtime()
    for i in range(8):
        pyautogui.hotkey('ctrl', '+')
        rtime(.5)
        if i == 4:  # 4 entspricht dem fünften durchlauf
            pyautogui.moveTo(2545, 488)
            sleep(.05)
            pyautogui.dragTo(2545, 968, duration=rtime(1, typing=True))
            rtime()
    rtime()


def login() -> bool:
    """
    logged_in = False
    check if website_loaded:
        logged_in = True
    elif btn1:
        btn1.click()
        waitfor(btn2)
        if btn2:
            btn2.click()
            waitfor(website_loaded)
            if website_loaded:
                logged_in = True
    return logged_in
    :return:
    """
    logged_in = False
    login_params = [
        {
            'id': 'logged_in', 'pic': r'pics\check_loaded_website.png', 'to_appear': True,
            'to_disappear': False, 'reg': (2, 1323, 148 - 1, 1439 - 1323), 'con': .9
        },
        {
            'id': 'login_button_1', 'pic': r'pics\login_button_1.png', 'to_appear': True,
            'to_disappear': False, 'reg': (1403, 739, 1831 - 1403, 882 - 739), 'con': .86
        },
        {
            'id': 'login_button_2', 'pic': r'pics\login_button_2.png', 'to_appear': True,
            'to_disappear': False, 'reg': (1044, 555, 1549 - 1044, 687 - 555), 'con': .9
        }
    ]
    clear_player_name_input_multi = wait_for_multiple(login_params, max_iterations=5, sleep_dur=1)
    if clear_player_name_input_multi.group():
        if clear_player_name_input_multi.hasattr('location'):
            id, location = clear_player_name_input_multi.group()

            if id == 'logged_in':
                logged_in = True
            elif id in ('login_button_1', 'login_button_2'):
                pyautogui.click(location)
                rtime(1)
                if id == 'login_button_1':
                    btn_2 = wait_for(
                        r'pics\login_button_2.png', reg=(1044, 555, 1549 - 1044, 687 - 555),
                        max_iterations=50, sleep_dur=.5
                    )
                    if btn_2:
                        pyautogui.click(btn_2)
                        rtime()
                    else: raise Exception('Fucked up Login')
                loaded_website = wait_for(
                    r'pics\check_loaded_website.png', reg=(2, 1323, 148 - 1, 1439 - 1323),
                    max_iterations=50, sleep_dur=.5
                )
                if loaded_website:
                    logged_in = True
    return logged_in


def kill_browser():
    window = win32ui.CreateWindowFromHandle(get_chrome_hwnd())
    window.PostMessage(win32con.WM_CLOSE, 0, 0)
    sleep(8)


if __name__ == '__main__':
    import os

    os.chdir('..')
    # open_web_app()
    # login()
    # zoom_in()
    kill_browser()
