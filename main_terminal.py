import os
import time
import threading
import random

def _getc():
    try:
        #  windows
        import msvcrt
        return msvcrt.getch()
    except ImportError:
        try:
            # max
            import Carbon
            if Carbon.Evt.EventAvail(0x0008)[0] == 0:  # 0x0008 is the keyDownMask
                return ''
            else:
                #
                # The event contains the following info:
                # (what,msg,when,where,mod)=Carbon.Evt.GetNextEvent(0x0008)[1]
                #
                # The message (msg) contains the ASCII char which is
                # extracted with the 0x000000FF charCodeMask; this
                # number is converted to an ASCII character with chr() and
                # returned
                #
                (what, msg, when, where, mod) = Carbon.Evt.GetNextEvent(0x0008)[1]
                return chr(msg & 0x000000FF)

        except:
            # unix
            import sys, tty, termios
            fd = sys.stdin.fileno()
            old_settings = termios.tcgetattr(fd)
            try:
                tty.setraw(sys.stdin.fileno())
                ch = sys.stdin.read(1)
            finally:
                termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            return ch

def _print(msg):
    print(msg, end='\r\n')

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

def cls():
    if os.name == 'nt':
        import subprocess
        tmp = subprocess.call('cls', shell=True)
    else:
        os.system('clear')

def key():
    c = _getc()
    if c is b'\xe0':
        c = _getc()
        if c is b'H':
            return UP
        elif c is b'P':
            return DOWN
        elif c is b'K':
            return LEFT
        elif c is b'M':
            return RIGHT
    if c is b'w':
        return UP
    elif c is b's':
        return DOWN
    elif c is b'a':
        return LEFT
    elif c is b'd':
        return RIGHT
    else:
        return c

last_key = None

class GameThread(threading.Thread):

    def __init__(self):
        threading.Thread.__init__ (self)
        self.running = True

        self.x = 20
        self.y = 40

        self.pos = [0, 0]
        self.ammo = 10
        self.bullets = []
        self.enemies = []

        self.frame = 0

        for i in range(5):
            self.addRandomEnemy()

        self.output = None

        self.setDaemon (True)

    def run(self):

        while self.running:

            self.clear()
            self.processInput()
            self.render()
            self.update()

            self.frame = self.frame + 1

            time.sleep(0.01)

    def clear(self):
        cls()

        # create new blank double array of spaces
        self.output = []
        for i in range(self.y):
            self.output.append(list(' ' * self.x))

    def processInput(self):
        global last_key

        if last_key is LEFT:
            self.pos[0] = (self.pos[0] - 1) % self.x
        if last_key is RIGHT:
            self.pos[0] = (self.pos[0] + 1) % self.x
        if last_key is UP:
            if(len(self.bullets) < 3 and self.ammo):
                self.ammo = self.ammo - 1
                self.bullets.append((self.pos[0], self.y - 2))

        last_key = None


    def render(self):

        # set cursor
        self.setPixel(self.pos[0], self.y-1, 'x')

        # set bullets
        for bullet in self.bullets:
            self.setPixel(bullet[0], bullet[1], '^')
            line = list('PHPSUCKS')
            for i in range(len(line)):
                y = bullet[1] + i + 1
                if(y < self.y-1):
                    self.setPixel(bullet[0], y, line[i])


        # set enemies
        for enemy in self.enemies:
            self.setPixel(enemy[0], enemy[1], '$')

        output = ""

        output = output + ('=' * (self.x+4)) + "\r\n"

        for row in self.output:
            output = output + ('| %s |' % ''.join(row)) + "\r\n"

        output = output + ('=' * (self.x + 4)) + "\r\n"
        output = output + ('Ammo: %s' % ('^' * self.ammo)) + "\r\n"

        # render board
        # _print('=' * (self.x+4))
        # for row in self.output:
        #     _print('| %s |' % ''.join(row))
        # _print('=' * (self.x + 4))
        # _print('Ammo: %s' % ('^' * self.ammo))
        print(output)

    def update(self):

        # add new enemies every 60 frames
        if self.frame % 60 is 0:
            self.addRandomEnemy()

        # move bullets upwards
        self.bullets = [(x,y-1) for x,y in self.bullets if y > 0]

        # check collisions
        hits = [i for i in self.bullets if i in self.enemies]
        # get new ammo per hit
        self.ammo = self.ammo + len(hits) * 3

        # remove collided bullets and enemies
        self.bullets = [i for i in self.bullets if i not in hits]
        self.enemies = [i for i in self.enemies if i not in hits]

        # move enemies every 60 frames
        if self.frame % 60 is 0:
            self.enemies = [(x,y+1) for x,y in self.enemies]

    def addRandomEnemy(self):
        enemy = (random.randint(0, self.x - 1), random.randint(0, 5))
        if enemy not in self.enemies:
            self.enemies.append(enemy)

    def setPixel(self, x, y, value):
        if 0 <= x < self.x and 0 <= y < self.y:
            self.output[y][x] = value
        else:
            raise ValueError('Out of bounds')

    def stop(self):
        self.running = False
        _print("stop running")


game = GameThread()
game.start()

while True:
    last_key = key()
    if last_key is b'q':
        break

print('end')