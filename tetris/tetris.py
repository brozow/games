# INTIALIZATION
import pygame, math, sys, random
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

    def moveUp(self):
        self.y = self.y -1

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
        self.drawAs(screen, self.color)
        
    def drawAs(self, screen, color):
        offsetX = self.board.getX()
        offsetY = self.board.getY()
        r = Rect((offsetX+self.x*BLOCK_SIZE, offsetY+self.y*BLOCK_SIZE), (BLOCK_SIZE, BLOCK_SIZE))
        pygame.draw.rect(screen, color, r)
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
        super(Block, self).moveLeft()
        for piece in self.pieces:
            piece.moveLeft()

    def moveRight(self):
        super(Block, self).moveRight()
        for piece in self.pieces:
            piece.moveRight()

    def moveDown(self):
        super(Block, self).moveDown()
        for piece in self.pieces:
            piece.moveDown()

    def moveUp(self):
        super(Block, self).moveUp()
        for piece in self.pieces:
            piece.moveUp()

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

    def rotateRight(self):
        pivot = self.pivot()
        if self.isHorizontal():
            self.rotateRightAround(pivot.x, pivot.y)
        else:
            self.rotateLeftAround(pivot.x, pivot.y)

    def rotateLeft(self):
        pivot = self.pivot()
        if self.isHorizontal():
            self.rotateRightAround(pivot.x, pivot.y)
        else:
            self.rotateLeftAround(pivot.x, pivot.y)        

            
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

    def rotateRight(self):
        pivot = self.pivot()
        if self.isHorizontal():
            self.rotateLeftAround(pivot.x, pivot.y)
        else:
            self.rotateRightAround(pivot.x, pivot.y)

    def rotateLeft(self):
        pivot = self.pivot()
        if self.isHorizontal():
            self.rotateLeftAround(pivot.x, pivot.y)
        else:
            self.rotateRightAround(pivot.x, pivot.y)   

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

    def rotateRight(self):
        pivot = self.pivot()
        if self.isHorizontal():
            self.rotateLeftAround(pivot.x, pivot.y)
        else:
            self.rotateRightAround(pivot.x, pivot.y)

    def rotateLeft(self):
        pivot = self.pivot()
        if self.isHorizontal():
            self.rotateLeftAround(pivot.x, pivot.y)
        else:
            self.rotateRightAround(pivot.x, pivot.y)   

    def pivot(self):
        return self.pieces[1]

class TetrisBoard:
    x = 0
    y = 0
    width = BLOCK_SIZE*10
    height = BLOCK_SIZE*20
    pieces = []
    deleting = []
    flashing = False
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

    def moveDown(self, block):
        block.moveDown()
        if not self.checkBounds(block) or self.overlaps(block):
            block.moveUp()
            self.addPieces(block.getPieces())
            return self.nextBlock()
        else:
            return block

    def moveLeft(self, block):
        block.moveLeft()
        if not self.checkBounds(block) or self.overlaps(block):
            block.moveRight();
        return block

    def moveRight(self, block):
        block.moveRight()
        if not self.checkBounds(block) or self.overlaps(block):
            block.moveLeft();
        return block
    
    def rotateLeft(self, block):
        block.rotateLeft()
        return block

    def rotateRight(self, block):
        block.rotateRight()
        return block

    def drop(self, block):
        while self.checkBounds(block) and not self.overlaps(block):
            block.moveDown()
        block.moveUp()
        self.addPieces(block.getPieces())
        
        return self.nextBlock()

    def nextBlock(self):
        n = random.randint(1,7)
        return {
          1: lambda : IBlock(self, 3, 0),
          2: lambda : JBlock(self, 3, 0),
          3: lambda : LBlock(self, 3, 0),
          4: lambda : SBlock(self, 3, 0),
          5: lambda : ZBlock(self, 3, 0),
          6: lambda : TBlock(self, 3, 0),
          7: lambda : OBlock(self, 3, 0),
        }[n]()
    
    def draw(self, screen):
        r = Rect((self.x, self.y),(self.width, self.height))
        pygame.draw.rect(screen, WHITE, r, 1)
        
        for piece in self.pieces:
            if self.flashing and self.deleting.count(piece.y):
                piece.drawAs(screen, WHITE)
            else:
                piece.draw(screen)


    def addPieces(self, pieces):
        self.pieces = self.pieces + pieces
        self.findFullRows()

    def getPiecesInRow(self, n):
        row = []
        for piece in self.pieces:
            if piece.y == n:
                row.append(piece)
        return row

    def getDeleting(self):
        return self.deleting

    def removeRow(self, n):

        def f(p): return p.y != n

        self.pieces = filter(f, self.pieces)
        
        for piece in self.pieces:
            if piece.y < n:
                piece.y = piece.y+1

    def removeDeleted(self):
        for n in self.deleting:
            self.removeRow(n)

        self.deleting = []

    def findFullRows(self):
        for n in range(0, 20):
            row = self.getPiecesInRow(n)
            if len(row) == 10:
                self.deleting.append(n)
        

    def checkBounds(self, block):
        for piece in block.getPieces():
            if piece.x < 0 or piece.x >= 10:
                return False
            if piece.y < 0 or piece.y >= 20:
                return False
        return True

    def overlaps(self, block):
        for boardPiece in self.pieces:
            for blockPiece in block.getPieces():
                if boardPiece.x == blockPiece.x and boardPiece.y == blockPiece.y:
                    return True
        return False

width = (1024-300)/2
height = (768-600)/2
board = TetrisBoard(width, height)
block = board.nextBlock()

screen = pygame.display.set_mode((1024, 768))

clock = pygame.time.Clock()
k_up = k_down = k_left = k_right = 0
speed = direction = 0
position = (100, 100)
TURN_SPEED = 5
ACCELERATION = 2
MAX_FORWARD_SPEED = 10
MAX_REVERSE_SPEED = -5

dropCount=0
deleteCount=0
DROP_TICKS = 30
DELETE_TICKS=5
DELETE_FLASHED=6
running = True

while running:
    # USER INPUT
    clock.tick(DROP_TICKS)
    
    deleting = board.getDeleting()
    #print "delete: %s" % deleting
    if len(deleting)> 0:
        deleteCount+=1

    if (deleteCount-1) % DELETE_TICKS == 0:
        board.flashing = not board.flashing

    if (deleteCount-1) // DELETE_TICKS >= DELETE_FLASHED:
        deleteCount = 0
        board.removeDeleted()
        
        
    dropCount+=1
    if dropCount >= DROP_TICKS:
        block=board.moveDown(block)
        dropCount=0
    for event in pygame.event.get():
        if not hasattr(event, 'key'): continue
        down = event.type == KEYDOWN # key down or up?
        if down and event.key == K_RIGHT: block=board.moveRight(block)
        elif down and event.key == K_LEFT: block=board.moveLeft(block)
        elif down and event.key == K_UP: block=board.rotateLeft(block)
        elif down and event.key == K_DOWN: block=board.rotateRight(block)
        elif down and event.key == K_SPACE: block=board.drop(block)
        elif down and event.key == K_ESCAPE: running = False
        elif down and event.key == K_o: block = OBlock(board, 4, 0)
        elif down and event.key == K_i: block = IBlock(board, 3, 0)
        elif down and event.key == K_l: block = LBlock(board, 3, 0)
        elif down and event.key == K_j: block = JBlock(board, 3, 0)
        elif down and event.key == K_s: block = SBlock(board, 3, 0)
        elif down and event.key == K_z: block = ZBlock(board, 3, 0)
        elif down and event.key == K_t: block = TBlock(board, 3, 0)
        elif down and event.key == K_q:
            board = TetrisBoard(width, height)
            block = board.nextBlock()
        elif down and event.key == K_EQUALS: DROP_TICKS -= 10
        elif down and event.key == K_MINUS: DROP_TICKS += 10
    screen.fill(BLACK)

    board.draw(screen)
    block.draw(screen)

    pygame.display.flip()

pygame.quit()
