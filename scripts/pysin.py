import os
import string

import clipboard as clipboard
import win32gui
import win32api
import pyautogui
from time import sleep
from random import randint

from numpy import iterable
from pynput import keyboard
from scripts.utils import rtime

hotkey_var = None

red = win32api.RGB(255, 49, 49)
blue = win32api.RGB(31, 81, 255)
orange = win32api.RGB(255, 95, 31)
green = win32api.RGB(15, 255, 80)
purple = win32api.RGB(188, 19, 254)


#
# def path(item):
#     return os.path.join(os.getcwd(), item)

# def _someKey():
#     """gets fired on press of hotkey"""
#     global hotkey_var
#     hotkey_var = "ctrl + someKey"


def _onHitAltS():
    """gets fired on press of hotkey"""
    global hotkey_var
    hotkey_var = "ctrl + alt + s"


def _onHitK():
    """this will immediately end the program; no excuses, no garbage collection whatsoever"""
    print('i was told to quit() immediately')
    os._exit(0)


def _hotkeyListener() -> keyboard.GlobalHotKeys:
    """declares hotkeys to listen to"""
    hot_listener = keyboard.GlobalHotKeys({
        # '<ctrl>+<someKey>': _someKey,
        '<ctrl>+<alt>+s': _onHitAltS,
        '<ctrl>+k': _onHitK})
    return hot_listener


def hotkey(shortcut: str) -> bool:
    """checks for latest pushed hotkey"""
    global hotkey_var
    if hotkey_var == shortcut:
        hotkey_var = None
        return True


def _random_rgb():
    r, g, b = randint(25, 100), randint(25, 100), randint(25, 100)
    return r, g, b


def _rgb_cycle(r, g, b):
    r += 1
    g += 1
    b += 1
    if r > 255 or g > 255 or b > 255:
        r, g, b = _random_rgb()
    # print(f'r: {r}, g: {g}, b: {b}')
    color = win32api.RGB(r, g, b)
    return color


def rtype(to_write: str, dur: int or float = 0, durs: list[int or float, ...] = None):
    if durs:
        for letter, dur in zip(to_write, durs):
            _type_foo(letter, dur)
    else:
        for letter in to_write:
            _type_foo(letter, dur)


def _type_foo(letter: str, dur: int or float):
    clipboard.copy(letter)
    sleep(.01)
    pyautogui.hotkey('ctrl', 'v')
    if letter not in string.ascii_letters:
        rtime(dur / 20)
    rtime(dur)
    # pyautogui.typewrite(letter, interval=rtime(dur, typing=True) / 6)


def _getInBetween(start: int, offset: int) -> list:
    """just some math"""
    temp_list = [start]
    for i in range(0, offset):
        temp_list.append(start + offset)
        offset -= 1
    temp_list.sort()
    return temp_list


def _widen(box: tuple[int, ...], widen=True) -> tuple[int, ...]:
    """so a second locate() would still find if border is still visible"""
    if box:
        x, y, xz, yz = box
        if widen:
            x -= 1
            y -= 1
            xz += 2
            yz += 2
        else:
            x += 5
            y += 5
            xz -= 10
            yz -= 10
        if pyautogui.onScreen(x, y) and pyautogui.onScreen(xz, yz):
            widened = x, y, xz, yz
        else:
            widened = box
        return widened


def _showBorder(box: tuple[int, ...], color: win32api.RGB = None, widen=True):
    """directly manipulate pixels on windows to show what pyautogui can see and more importantly where"""
    if not color:
        color = orange
    if box:
        x, y, xz, yz = _widen(box, widen)
        xt = _getInBetween(x, xz)
        yt = _getInBetween(y, yz)
        fucked_up = None
        try:
            dc = win32gui.GetDC(0)
            for a in xt:
                win32gui.SetPixel(dc, a, y, color)
            for b in yt:
                win32gui.SetPixel(dc, x, b, color)
            for c in xt:
                win32gui.SetPixel(dc, c, y + yz, color)
            for d in yt:
                win32gui.SetPixel(dc, x + xz, d, color)
        except Exception as e:
            fucked_up = e
        if fucked_up:
            # print(f'showBorder has fucked up, because: {fucked_up}')
            pass


def wait_for(
        pic: str, con: float = .9, reg: tuple = None, debug: bool = True,
        appear: bool = True, disappear: bool = False, max_iterations: int = 10, sleep_dur: int or float = 1
) -> tuple[int, ...] or 'bool':
    """
    either appear or disappear has to be True
    :param pic:
    :param con:
    :param reg:
    :param debug:
    :param appear:
    :param disappear:
    :param max_iterations:
    :param sleep_dur:
    :return:
    """
    out = None
    for i in range(max_iterations):
        location = locate(pic, con=con, reg=reg, debug=debug)
        if not appear and not disappear:
            raise Exception('either appear or disappear has to be True')
        if appear:
            if location:
                out = location
                break
        elif disappear:
            if not location:
                out = not location
                break
        sleep(sleep_dur)
    return out


class Multiple:
    def __init__(self):
        self._group = False

    def hasattr(self, attr: str):
        if attr == 'location':
            if self._group is not None and isinstance(self._group, tuple):
                return True

    def _set_group(self, value: tuple[int, ...] or bool):
        self._group = value

    def group(self) -> tuple[str, tuple[int, ...]] or bool:
        return self._group


def wait_for_multiple(
        pic_kwargs: list[dict[str or float or int or tuple[int, ...] or bool]],
        max_iterations: int = 10, sleep_dur: int or float = 1
) -> Multiple:
    """

    example params: [
        {
            'id': str,
            'pic': str,
            'con': float or int,
            'reg': tuple,
            'to_appear': bool,
            'to_disappear': bool
        },
        ...
    ]

    returns Multiple, access like this:
        result = wait_for_multiple(params)
        if result.group():
            if result.hasattr('location'):
                id, (x, y, xz, yz) = result.group()
            ...

    :param pic_kwargs:
    :param max_iterations:
    :param sleep_dur:
    :return:
    """
    output = Multiple()
    for i in range(max_iterations):
        for kwargs in pic_kwargs:
            location = locate(pic=kwargs['pic'], con=kwargs['con'], reg=kwargs['reg'])
            if not kwargs['to_appear'] and not kwargs['to_disappear']:
                raise Exception('either to_appear or to_disappear has to be True')
            if kwargs['to_appear']:
                if location:
                    output._set_group((kwargs['id'], location))
                    break
            elif kwargs['to_disappear']:
                if not location:
                    output._set_group(True)
                    break
        if output.group():
            break
        sleep(sleep_dur)
    return output


def locate(
        pic: str, con: float = .9, reg: tuple[int, ...] = None,
        debug: bool = True, widen: bool = True, gray: bool = False
) -> tuple[int, ...]:
    """returns first appearance of screenshot"""
    if '.png' not in pic:
        pic = f'{pic}.png'
    if not reg:
        reg = 0, 0, 1919, 1079
    if debug:
        _showBorder(reg, purple)  # purple = total area to look in
    location = pyautogui.locateOnScreen(pic, confidence=con, region=reg, grayscale=gray)
    if debug:
        if location:
            _showBorder(location, green, widen=widen)  # green = found
        else:
            _showBorder(reg, red)  # red = not found
    return location


def locate_consecutively(
        pic: str, con: float, reg: tuple[int, ...], direction: str = 'down', debug=True, widen=True
) -> list[tuple[int, ...]]:
    locations = []
    adjusted_reg = reg
    x1, y1, xz1, yz1 = reg
    while True:
        try:
            location = locate(pic, con, adjusted_reg, debug, widen)
            # print(location)
        except ValueError:
            location = None
        if location:
            locations.append(location)
            x2, y2, xz2, yz2 = location
            if direction == 'down':
                adjusted_reg = x1, y1 + (y2 - y1) + yz2, xz1, yz1 - ((y2 - y1) + yz2)
            elif direction == 'right':
                pass
                # new_x = x1 + (x2 + xz2) - int(xz2 / 2)
                # new_y = y1
                # new_xz = xz1 - (xz2 - x1) + int(xz2 / 2)
                # new_yz = yz1
                # adjusted_reg = new_x, new_y, new_xz, new_yz
                # print(adjusted_reg)
                # sleep(1)
        else:
            break
    return locations


def read_number(size, reg):
    topf = []
    for num in string.digits:
        for location in locate_consecutively(
                rf'pics\numbers\{size}\{num}.png', .85, reg, 'right', debug=True, widen=False
        ):
            # print(num)
            topf.append((location, num))
    if topf:
        topf = sorted(topf)
        # for num, name in topf:
        #     color = _rgb_cycle(*_random_rgb())
        #     _showBorder(num, color)

        return int(''.join(name for num, name in topf))


def locateAll(pic: str, con: float = .9, reg: tuple[int, ...] = None, debug: bool = False) -> list[tuple[int, ...]]:
    """returns all appearances of screenshot"""
    if '.png' not in pic:
        pic = f'{pic}.png'
    if not reg:
        reg = 0, 0, 1919, 1079
    if debug:
        _showBorder(reg, purple)
    locations = list(pyautogui.locateAllOnScreen(pic, confidence=con, region=reg))
    locations2 = list(locations)
    if debug:
        if locations:
            for location in locations:
                color = _rgb_cycle(*_random_rgb())
                _showBorder(location, color)
        else:
            _showBorder(reg, red)
    return locations2


def testConfidence(pic: str, con: float = 1, reg: tuple[int, ...] = None, print_color: bool = True):
    """input: path/to/pic -> try which confidence suits best"""
    from datetime import datetime
    from time import sleep

    if '.png' not in pic:
        pic = f'{pic}.png'
    if not reg:
        reg = 0, 0, 1919, 1079

    while True:
        con -= .01
        if con < .5:
            break
        str_con = str(con)
        str_con = str_con[:4]
        con = float(str_con)
        start = datetime.now()

        hexagons = locateAll(pic, con=con, reg=reg, debug=True)
        length = 0
        if hexagons:
            length = len(hexagons)

        end = datetime.now()

        delta = end - start

        if print_color:
            to_print = f't: {delta}, con: {con}'
            if length > 0:
                to_print += f', results: {length}'
            print(to_print)
        sleep(1)
        # u might need to change these locations to suit your needs
        pyautogui.rightClick(454, 285)  # right click on desktop
        sleep(.25)
        pyautogui.click(503, 345)  # refresh
        sleep(1)


# this will always run
_hotkeyListener().start()

# this will only run if this script is run directly
if __name__ == '__main__':
    os.chdir('..')
    import clipboard
    # testConfidence('hexagon', con=1, reg=(366,0,1684-366,1079-0), print_color=True)
    # locate_consecutively(r'..\pics\white_arrow.png', .9, (1502, 411, 1613-1502, 1268-411))
    # print('big: ', read_number(size='big_num', reg=(627, 908, 843 - 627, 1074 - 908)))
    # print('small1: ', read_number(size='small_num', reg=(1281, 936, 1462 - 1281, 1033 - 936)))
    # print('small2: ', read_number(size='small_num', reg=(1201, 1060, 1370 - 1201, 1164 - 1060)))
    # print('tiny: ', read_number(size='tiny_num', reg=(1769, 306, 2218 - 1769, 389 - 306)))
    """
    string = clipboard.paste()
    args = string.split('\', reg=(')
    pic = args[0]
    region = args[1][:-1]
    region = region.split(', ')
    print(pic)
    print(region)
    x = eval(region[0])
    y = eval(region[1])
    xz = eval(region[2])
    yz = eval(region[3])
    region = x, y, xz, yz
    """
    con = .8
    pic = r'pics\no_player_name.png'
    region = (1202, 437, 1457 - 1202, 531 - 437)
    for i in range(20):
        print(f'{con = }')
        gray = locate(pic, gray=True, con=con, reg=(region))
        rgb = locate(pic, gray=False, con=con, reg=(region))
        print(f'{gray}')
        print(f'{rgb}')
        if not gray and not rgb: break
        con += .01
