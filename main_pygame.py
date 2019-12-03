# import the pygame module, so you can use it
import pygame
import random

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

ENEMY_COLOR = (255, 0, 0)
CURSOR_COLOR = (0, 0, 255)
BULLET_COLOR = (0,255,0)
AMMO_COLOR = (0,255,255)

# define a main function
def main():

    # initialize the pygame module
    pygame.init()
    pygame.font.init()

    # load and set the logo
    # logo = pygame.image.load("logo32x32.png")
    # pygame.display.set_icon(logo)
    pygame.display.set_caption("Pew Pew")

    # create a surface on screen that has the size of 240 x 180
    gridsize = 16
    gridwidth = 20
    gridheight = 40

    game = Game(gridwidth, gridheight, gridsize)

    screen_width = gridwidth * gridsize
    screen_height = gridheight * gridsize
    screen = pygame.display.set_mode((screen_width, screen_height))

    background_image = pygame.image.load("background.png")

    # update the screen to make the changes visible (fullscreen update)
    pygame.display.flip()

    # a clock for controlling the fps later
    clock = pygame.time.Clock()



    # define a variable to control the main loop
    running = True
    # main loop
    while running:
        # event handling, gets all event from the eventqueue
        for event in pygame.event.get():
            # only do something if the event if of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                running = False
            # check for keypress and check if it was Esc
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.processInput(UP)
                if event.key == pygame.K_DOWN:
                    game.processInput(DOWN)
                if event.key == pygame.K_LEFT:
                    game.processInput(LEFT)
                if event.key == pygame.K_RIGHT:
                    game.processInput(RIGHT)

        for x in range(0,screen_width,320):
            for y in range(0,screen_height,240):
                screen.blit(background_image, (x,y))


        game.render(screen)

        pygame.display.flip()

        game.update()
        clock.tick(10)




class Game():

    def __init__(self, width, height, gridsize):
        self.x = width
        self.y = height
        self.gridsize = gridsize

        self.pos = [0, 0]
        self.ammo = 10
        self.bullets = []
        self.enemies = []

        self.frame = 0

        for i in range(5):
            self.addRandomEnemy()

    def processInput(self, key):

        if key is LEFT:
            self.pos[0] = (self.pos[0] - 1) % self.x
        if key is RIGHT:
            self.pos[0] = (self.pos[0] + 1) % self.x
        if key is UP:
            if(len(self.bullets) < 3 and self.ammo):
                self.ammo = self.ammo - 1
                self.bullets.append((self.pos[0], self.y - 2))

    def render(self, screen):

        # set cursor
        self.setPixel(self.pos[0], self.y-1, CURSOR_COLOR, screen)

        # set bullets
        for bullet in self.bullets:
            self.setPixel(bullet[0], bullet[1], BULLET_COLOR, screen)
            line = list('PHPSUCKS')

            myfont = pygame.font.SysFont('Comic Sans MS', 18)

            for i in range(len(line)):
                y = bullet[1] + i + 1
                if(y < self.y-1):

                    self.setPixel(bullet[0], y, BULLET_COLOR, screen)

                    textsurface = myfont.render(line[i], False, (0, 0, 0))
                    screen.blit(textsurface,(bullet[0]*self.gridsize,y*self.gridsize))

                    # self.setPixel(bullet[0], y, line[i], screen)



        # set enemies
        for enemy in self.enemies:
            self.setPixel(enemy[0], enemy[1], ENEMY_COLOR, screen)

        for i in range(self.ammo):
            self.setPixel(self.x - 1, self.y - 1 - i , AMMO_COLOR, screen)

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

        self.frame = self.frame + 1

    def addRandomEnemy(self):
        enemy = (random.randint(0, self.x - 1), random.randint(0, 5))
        if enemy not in self.enemies:
            self.enemies.append(enemy)

    def setPixel(self, x, y, color, screen):
        if 0 <= x < self.x and 0 <= y < self.y:
            pygame.draw.rect(screen,color,(x*self.gridsize,y*self.gridsize,self.gridsize,self.gridsize))
        else:
            raise ValueError('Out of bounds')

# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
