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
    """ x and y are 'grid coordinates'"""
    """ upper left corner is 0,0 """
    """ board is 10 wide ( x direction ) """
    """ and 20 high ( y direction ) """
    x = 0
    y = 0
    """ 0 is initial position """
    """ 1 is rotated clockwise from initial position 90 degrees """
    """ 2 is rotated clockwise 180 degrees """
    """ 3 is rotated clockwise 270 degrees """
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
        self.y = 19

    def rotateRight(self):
        self.orientation = (self.orientation + 1) % 4

    def rotateLeft(self):
        self.orientation = (self.orientation - 1) % 4 

    def isHorizontal(self):
        return self.orientation == 0 or self.orientation == 2

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

    def rotateRightAround(self, x, y):
        dx = self.x - x
        dy = self.y - y
        self.x = x - dy
        self.y = y + dx

    def rotateLeftAround(self, x, y):
        dx = self.x - x
        dy = self.y - y
        self.x = x + dy
        self.y = y - dx

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

    def bounds(self):
        raise NotImplementedError("Please Implement bounds")        

    def getPieces(self):
        return self.pieces

    def rotateRightAround(self, pivotX, pivotY):
        for piece in self.pieces:
            piece.rotateRightAround(pivotX, pivotY)

        super(Block, self).rotateRight();
        
    def rotateLeftAround(self, pivotX, pivotY):
        for piece in self.pieces:
            piece.rotateLeftAround(pivotX, pivotY)

        super(Block, self).rotateLeft()

    def rotateRight(self):
        pivot = self.pivot()
        if pivot == None:
            super(Block, self).rotateRight()
        else:
            self.rotateRightAround(pivot.x, pivot.y)

    def rotateLeft(self):
        pivot = self.pivot()
        if pivot == None:
            super(Block, self).rotateLeft()
        else:
            self.rotateLeftAround(pivot.x, pivot.y)

    def moveLeft(self):
        b = self.bounds()
        if b.left == 0:
            return
        super(Block, self).moveLeft()
        for piece in self.pieces:
            piece.moveLeft()

    def moveRight(self):
        b = self.bounds()
        if b.right == 10:
            return
        super(Block, self).moveRight()
        for piece in self.pieces:
            piece.moveRight()

    def moveDown(self):
        b = self.bounds()
        if b.bottom == 20:
            return
        super(Block, self).moveDown()
        for piece in self.pieces:
            piece.moveDown()

    def drop(self):
        b = self.bounds()
        while b.bottom < 20:
            self.moveDown()
            b = self.bounds()

    def draw(self, screen):
        for piece in self.pieces:
            piece.draw(screen)


#"""the O"""
class OBlock(Block):
    def __init__(self, board, x, y):
        super(OBlock, self).__init__(board,x,y,[Piece(board,x,y,YELLOW), Piece(board,x+1,y,YELLOW), Piece(board,x,y+1,YELLOW), Piece(board,x+1,y+1,YELLOW)])

    def bounds(self):
        r = Rect((self.x,self.y),(2,2))
        #print r, r.top, r.left, r.right, r.bottom
        return r

    def pivot(self):
        return None

#"""the I"""
class IBlock(Block):
    def __init__ (self, board, x, y):
        super(IBlock, self).__init__(board,x,y,[Piece(board,x,y,CYAN), Piece(board,x+1,y,CYAN), Piece(board,x+2,y,CYAN), Piece(board,x+3,y,CYAN)])

    def bounds(self):
        if self.isHorizontal():
            r = Rect((self.x, self.y), (4,1))
        else:
            r = Rect((self.x, self.y), (1,4))
        return r

    def pivot(self):
        return self.pieces[1]

            
#"""the J"""
class JBlock(Block):
    def __init__ (self, board, x, y):
        super(JBlock, self).__init__(board,x,y,[Piece(board,x,y,BLUE), Piece(board,x+1,y,BLUE), Piece(board,x+2,y,BLUE), Piece(board,x+2,y+1,BLUE)])

    def bounds(self):
        if self.isHorizontal():
            r = Rect((self.x, self.y), (3,2))
        else:
            r = Rect((self.x, self.y), (2,3))
        return r

    def pivot(self):
        return self.pieces[1]

#"""the L"""
class LBlock(Block):
    def __init__ (self, board, x, y):
        super(LBlock, self).__init__(board,x,y,[Piece(board,x,y,ORANGE), Piece(board,x+1,y,ORANGE), Piece(board,x+2,y,ORANGE), Piece(board,x,y+1,ORANGE)])


    def bounds(self):
        if self.isHorizontal():
            r = Rect((self.x, self.y), (3,2))
        else:
            r = Rect((self.x, self.y), (2,3))
        return r

    def pivot(self):
        return self.pieces[1]

#"""the T"""
class TBlock(Block):
    def __init__ (self, board, x, y):
        super(TBlock, self).__init__(board,x,y,[Piece(board,x,y,MAGENTA), Piece(board,x+1,y,MAGENTA), Piece(board,x+2,y,MAGENTA), Piece(board,x+1,y+1,MAGENTA)])


    def bounds(self):
        if self.isHorizontal():
            r = Rect((self.x, self.y), (3,2))
        else:
            r = Rect((self.x, self.y), (2,3))
        return r

    def pivot(self):
        return self.pieces[1]

#"""the S"""
class SBlock(Block):
    def __init__ (self, board, x, y):
        super(SBlock, self).__init__(board,x,y,[Piece(board,x,y+1,GREEN), Piece(board,x+1,y+1,GREEN), Piece(board,x+1,y,GREEN), Piece(board,x+2,y,GREEN)])
 

    def bounds(self):
        if self.isHorizontal():
            r = Rect((self.x, self.y), (3,2))
        else:
            r = Rect((self.x, self.y), (2,3))
        return r

    def pivot(self):
        return self.pieces[2]

#"""the Z"""
class ZBlock(Block):
    def __init__ (self, board, x, y):
        super(ZBlock, self).__init__(board,x,y,[Piece(board,x,y,RED), Piece(board,x+1,y,RED), Piece(board,x+1,y+1,RED), Piece(board,x+2,y+1,RED)])


    def bounds(self):
        if self.isHorizontal():
            r = Rect((self.x, self.y), (3,2))
        else:
            r = Rect((self.x, self.y), (2,3))
        return r

    def pivot(self):
        return self.pieces[1]

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
block = IBlock(board, 3,0)
doneBlock = IBlock(board, 3,19)
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
        if down and event.key == K_RIGHT: block.moveRight()
        elif down and event.key == K_LEFT: block.moveLeft()
        elif down and event.key == K_UP: block.rotateLeft()
        elif down and event.key == K_DOWN: block.rotateRight()
        elif down and event.key == K_SPACE: block.drop()
        elif down and event.key == K_ESCAPE: sys.exit(0) # quit the game
        elif down and event.key == K_o: block = OBlock(board, 4, 0)
        elif down and event.key == K_i: block = IBlock(board, 3, 0)
        elif down and event.key == K_l: block = LBlock(board, 3, 0)
        elif down and event.key == K_j: block = JBlock(board, 3, 0)
        elif down and event.key == K_s: block = SBlock(board, 3, 0)
        elif down and event.key == K_z: block = ZBlock(board, 3, 0)
        elif down and event.key == K_t: block = TBlock(board, 3, 0)
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
    block.draw(screen)

    pygame.display.flip()
