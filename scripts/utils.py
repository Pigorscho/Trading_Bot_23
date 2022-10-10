from time import sleep
from random import randint

test = False


def rtime(duration: int or float = 0, typing: bool = False):
    c1 = .000006812565271824563
    c2 = .0000004828437685345364
    c3 = .0000017652435463434
    r1 = randint(7500, 42000)
    r2 = randint(7500, 42000)
    r3 = randint(7500, 42000)
    r = (r1 * c1) + (r2 * c2) + (r3 * c3) + duration
    if not test:
        sleep(r)
    if test or typing:
        return r


if __name__ == '__main__':
    for i in range(100):
        print(rtime(0))
