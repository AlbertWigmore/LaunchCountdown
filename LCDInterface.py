import LCDDriver
import threading
from time import sleep


class LCDInterface():
    def __init__(self):
        self.lcd = LCDDriver.lcd()
        self.lcd.lcd_clear()

        self.lines = ['', '', '', '']
        self.clear()
        self.isrunning = False
        self.offsets = [0, 0, 0, 0]

    def clear(self):
        self.write(['', '', '', ''])

    def write(self, lines, align=str.ljust):
        for i, x in enumerate(lines):
            self.write_line(i, x, align=align)

    def write_line(self, line_no, line, align=str.ljust):
        self.lines[line_no] = align(line, 20)

    def strobe(self):
        pass

    def run(self):
        while self.isrunning:
            for i, x in enumerate(self.lines):
                j = self.offsets[i]
                self.offsets[i] = (j+1) % (len(x)-19 if len(x) > 20 else 1)
                self.lcd.lcd_display_string(x[j:j+20], i+1)
            sleep(0.4)

    def start(self):
        if not self.isrunning:
            self.isrunning = True
            threading.Thread(target=LCDInterface.run,
                             args=[self]).start()

    def stop(self):
        self.isrunning = False

    def update(self):
        pass


if __name__ == '__main__':
    c = LCDInterface()
    try:
        c.write(['Hi', 'I am', 'an', 'Orange'], align=str.center)
        c.start()
        while True:
            pass
    finally:
        c.stop()
