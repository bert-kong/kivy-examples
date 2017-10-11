__author__ = 'bckong'

import threading
import time

loading_done = False
con = threading.Condition()


def loader(con):
    con.acquire()
    time.sleep(3)
    global loading_done
    loading_done = True
    con.notifyAll()
    con.release()


msg= {
    0:"\rStart Python SV Session ",
    1:"\rStart Python SV Session ..",
    2:"\rStart Python SV Session .....",
    3:"\rStart Python SV Session ........",
    4:"\rStart Python SV Session ............",
    5:"\rStart Python SV Session ..................",
}
def print_spinner():
    cnt = 0
    spin_cnt = 0
    while True:
        print msg[spin_cnt] + ","
        time.sleep(.3)
        spin_cnt = (spin_cnt + 1)%6


if __name__ == '__main__':
    print_spinner()
