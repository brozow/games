# INTIALISATION
import pygame, math, sys
from pygame.locals import *

class Block:
    """tile = pygame.image.load('tile.png')"""
    """A block class"""
    x = 0
    y = 0
    orientation = 0
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def moveLeft(self):
        self.x = self.x -1

    def moveRight(self):
        self.x = self.x +1

    def moveDown(self):
        self.y = self.y +1

    def drop(self):
        self.y = 20

    def rotateRight(self):
        self.orientation = (self.orientation + 1) % 4

    def rotateLeft(self):
        self.orientation = (self.orientation - 1) % 4 

    def draw(self, screen):
        raise NotImplementedError("Please Implement Draw Function")

    def checkPosition(self):
        raise NotImplementedError("Please Implement checkPosition")
        
class OBlock(Block):
    #def __init__ (self, x, y):
     #   super(OBlock, self).__init__(x,y)

    def draw(self, screen):
        pygame.draw.rect(screen, (255,0,0), Rect((50,50), (60,60)))

#"""the O"""
#"""the I"""
#"""the J"""
#"""the L"""
#"""the T"""
#"""the S"""
#"""the Z"""

oblock = OBlock(0,0)
screen = pygame.display.set_mode((1024, 768))
car = pygame.image.load('car.png')
clock = pygame.time.Clock()
k_up = k_down = k_left = k_right = 0
speed = direction = 0
position = (100, 100)
TURN_SPEED = 5
ACCELERATION = 2
MAX_FORWARD_SPEED = 10
MAX_REVERSE_SPEED = -5
BLACK = (255,0,255)
while 1:
    # USER INPUT
    clock.tick(30)
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN # key down or up?
        if event.key == K_RIGHT: k_right = down * -TURN_SPEED
        elif event.key == K_LEFT: k_left = down * TURN_SPEED
        elif event.key == K_UP: k_up = down * ACCELERATION
        elif event.key == K_DOWN: k_down = down * -ACCELERATION
        elif event.key == K_ESCAPE: sys.exit(0) # quit the game
    screen.fill(BLACK)

    # SIMULATION
    # .. new speed and direction based on acceleration and turn
    speed += (k_up + k_down)
    if speed > MAX_FORWARD_SPEED: speed = MAX_FORWARD_SPEED
    if speed < MAX_REVERSE_SPEED: speed = MAX_REVERSE_SPEED
    direction += (k_right + k_left)
    # .. new position based on current position, speed and direction
    x, y = position
    rad = direction * math.pi / 180
    x += -speed*math.sin(rad)
    y += -speed*math.cos(rad)
    position = (x, y)

    # RENDERING
    # .. rotate the car image for direction
    rotated = pygame.transform.rotate(car, direction)
    # .. position the car on screen
    rect = rotated.get_rect()
    rect.center = position
    # .. render the car to screen
    screen.blit(rotated, rect)
    oblock.draw(screen)
    pygame.display.flip()
