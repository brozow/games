# INTIALIZATION
import pygame, math, sys
from pygame.locals import *

RED = (255,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
CYAN = (0,255,255)
ORANGE = (255,127,0)
YELLOW = (255,255,0)
MAGENTA = (255,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)

BLOCK_SIZE = 30

class Figure(object):
    board = None
    x = 0
    y = 0
    orientation = 0
    def __init__(self, board, x, y):
        self.board = board
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

class Piece(Figure):
    """tile = pygame.image.load('tile.png')"""
    """A square that makes up a block"""
    color = (255,0,0)
    
    def __init__(self, board, x, y, color):
        super(Piece, self).__init__(board, x,y)
        self.color = color

    def draw(self, screen):
        offsetX = self.board.getX()
        offsetY = self.board.getY()
        r = Rect((offsetX+self.x*BLOCK_SIZE, offsetY+self.y*BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, self.color, r)
        pygame.draw.rect(screen, WHITE, r, 1)

class Block(Figure):
    
    def __init__(self, board, x, y, pieces):
        super(Block, self).__init__(board,x,y)
        self.pieces = pieces

    def getPieces(self):
        return self.pieces

    def draw(self, screen):
        for piece in self.pieces:
            piece.draw(screen)


#"""the O"""
class OBlock(Block):
    def __init__(self, board, x, y):
        super(OBlock, self).__init__(board,x,y,[Piece(board,x,y,YELLOW), Piece(board,x+1,y,YELLOW), Piece(board,x,y+1,YELLOW), Piece(board,x+1,y+1,YELLOW)])
    

#"""the I"""
class IBlock(Block):
    def __init__ (self, board, x, y):
        super(IBlock, self).__init__(board,x,y,[Piece(board,x,y,CYAN), Piece(board,x+1,y,CYAN), Piece(board,x+2,y,CYAN), Piece(board,x+3,y,CYAN)])

#"""the J"""
class JBlock(Block):
    def __init__ (self, board, x, y):
        super(JBlock, self).__init__(board,x,y,[Piece(board,x,y,BLUE), Piece(board,x+1,y,BLUE), Piece(board,x+2,y,BLUE), Piece(board,x+2,y+1,BLUE)])

#"""the L"""
class LBlock(Block):
    def __init__ (self, board, x, y):
        super(LBlock, self).__init__(board,x,y,[Piece(board,x,y,ORANGE), Piece(board,x+1,y,ORANGE), Piece(board,x+2,y,ORANGE), Piece(board,x,y+1,ORANGE)])

#"""the T"""
class TBlock(Block):
    def __init__ (self, board, x, y):
        super(TBlock, self).__init__(board,x,y,[Piece(board,x,y,MAGENTA), Piece(board,x+1,y,MAGENTA), Piece(board,x+2,y,MAGENTA), Piece(board,x+1,y+1,MAGENTA)])

#"""the S"""
class SBlock(Block):
    def __init__ (self, board, x, y):
        super(SBlock, self).__init__(board,x,y,[Piece(board,x,y+1,GREEN), Piece(board,x+1,y+1,GREEN), Piece(board,x+1,y,GREEN), Piece(board,x+2,y,GREEN)])
 
#"""the Z"""
class ZBlock(Block):
    def __init__ (self, board, x, y):
        super(ZBlock, self).__init__(board,x,y,[Piece(board,x,y,RED), Piece(board,x+1,y,RED), Piece(board,x+1,y+1,RED), Piece(board,x+2,y+1,RED)])

class TetrisBoard:
    x = 0
    y = 0
    width = BLOCK_SIZE*10
    height = BLOCK_SIZE*20
    pieces = []
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height
    
    def draw(self, screen):
        r = Rect((self.x, self.y),(self.width, self.height))
        pygame.draw.rect(screen, WHITE, r, 1)
        
        for piece in self.pieces:
            piece.draw(screen)

    def addPieces(self, pieces):
        self.pieces = self.pieces + pieces
    
board = TetrisBoard((1024-300)/2, (786-600)/2)
oblock = OBlock(board, 0,0)
iblock = IBlock(board, 2,2)
jblock = JBlock(board, 6,3)
lblock = LBlock(board, 9,5)
tblock = TBlock(board, 12,6)
sblock = SBlock(board, 15,6)
zblock = ZBlock(board, 18,7)
doneBlock = IBlock(board, 3,19)
board.addPieces(doneBlock.getPieces())
doneBlock = LBlock(board, 4, 17)
board.addPieces(doneBlock.getPieces())
screen = pygame.display.set_mode((1024, 768))
#car = pygame.image.load('car.png')
clock = pygame.time.Clock()
k_up = k_down = k_left = k_right = 0
speed = direction = 0
position = (100, 100)
TURN_SPEED = 5
ACCELERATION = 2
MAX_FORWARD_SPEED = 10
MAX_REVERSE_SPEED = -5

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
 #   rotated = pygame.transform.rotate(car, direction)
    # .. position the car on screen
 #   rect = rotated.get_rect()
 #   rect.center = position
    # .. render the car to screen
 #   screen.blit(rotated, rect)
    board.draw(screen)
    oblock.draw(screen)
    iblock.draw(screen)
    jblock.draw(screen)
    lblock.draw(screen)
    tblock.draw(screen)
    sblock.draw(screen)
    zblock.draw(screen)
    pygame.display.flip()
