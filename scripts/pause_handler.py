from random import randint

from scripts.utils import rtime


def auto_pause():
    mins = randint(51, 69)
    for min in range(mins):
        for sec in range(60):
            print(f'mins: {mins}/{str(min).zfill(2)} | secs: 60/{str(sec).zfill(2)}', end='\r')
            for about_a_sec in range(4):
                rtime()
    for being_sure in range(42):
        rtime(randint(10, 99) / 100)
    print('ending autopause')


def no_player_found_pause():
    for sec in range(60):
        for about_a_sec in range(4):
            rtime()


if __name__ == '__main__':
    print('4', rtime(typing=True) + rtime(typing=True) + rtime(typing=True) + rtime(typing=True))  # ~ 1 sec
