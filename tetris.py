from graphics import *
import random


############################################################
# BLOCK CLASS
############################################################
class Block(Rectangle):
    ''' Block class:
        Implement a block for a tetris piece
        Attributes: x - type: int
                    y - type: int
        specify the position on the tetris board
        in terms of the square grid
    '''
    BLOCK_SIZE = 30
    # BLOCK_SIZE = 29
    OUTLINE_WIDTH = 3

    def __init__(self, pos, color):
        self.x = pos.x
        self.y = pos.y

        p1 = Point(pos.x*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH,
                   pos.y*Block.BLOCK_SIZE + Block.OUTLINE_WIDTH)
        p2 = Point(p1.x + Block.BLOCK_SIZE, p1.y + Block.BLOCK_SIZE)

        Rectangle.__init__(self, p1, p2)
        self.setWidth(Block.OUTLINE_WIDTH)
        self.setFill(color)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool

            checks if the block can move dx squares in the x direction
            and dy squares in the y direction
            Returns True if it can, and False otherwise
            HINT: use the can_move method on the Board object
        '''
        if board.can_move(self.x+dx, self.y+dy):
            return True
        else:
            return False

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the block dx squares in the x direction
            and dy squares in the y direction
        '''
        self.x += dx
        self.y += dy

        Rectangle.move(self, dx*Block.BLOCK_SIZE, dy*Block.BLOCK_SIZE)


############################################################
# SHAPE CLASS
############################################################
class Shape():
    ''' Shape class:
        Base class for all the tetris shapes
        Attributes: blocks - type: list - the list of blocks making up the shape
                    rotation_dir - type: int - the current rotation direction of the shape
                    shift_rotation_dir - type: Boolean - whether or not the shape rotates
    '''

    def __init__(self, coords, color):
        self.blocks = []
        self.rotation_dir = -1
        ### A boolean to indicate if a shape shifts rotation direction or not.
        ### Defaults to false since only 3 shapes shift rotation directions (I, S and Z)
        self.shift_rotation_dir = False

        for pos in coords:
            self.blocks.append(Block(pos, color))

    def get_blocks(self):
        '''returns the list of blocks'''
        return self.blocks

    def draw(self, win):
        ''' Parameter: win - type: CanvasFrame

            Draws the shape:
            i.e. draws each block
        '''
        for block in self.blocks:
            block.draw(win)

    def move(self, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            moves the shape dx squares in the x direction
            and dy squares in the y direction, i.e.
            moves each of the blocks
        '''
        for block in self.blocks:
            block.move(dx, dy)

    def can_move(self, board, dx, dy):
        ''' Parameters: dx - type: int
                        dy - type: int

            Return value: type: bool

            checks if the shape can move dx squares in the x direction
            and dy squares in the y direction, i.e.
            check if each of the blocks can move
            Returns True if all of them can, and False otherwise

        '''
        for block1 in self.blocks:
            check = block1.can_move(board, dx, dy)
            if check:
                continue
            else:
                break
        return check

    def get_rotation_dir(self):
        ''' Return value: type: int

            returns the current rotation direction
        '''
        return self.rotation_dir

    def can_rotate(self, board):
        ''' Parameters: board - type: Board object
            Return value: type : bool

            Checks if the shape can be rotated.

            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation and check if
            the new position is valid
            3. If any of the blocks cannot be moved to their new position,
            return False

            otherwise all is good, return True
        '''
        direction = self.get_rotation_dir()
        # print 'Direction:', direction
        for block in self.blocks:
            old_x = block.x
            old_y = block.y
            centre = self.blocks[1]
            # print block, 'Old Co-ordinates:', old_x, old_y
            # print 'New Co-ordinates:', centre.x-direction*centre.y+direction*block.y, '   ', centre.y+direction*centre.x-direction*block.x
            check = board.can_move(centre.x-direction*centre.y+direction*block.y, centre.y+direction*centre.x-direction*block.x)
            # print 'check:', check
            if check:
               continue
            else:
               break
        return check

    def rotate(self, board):
        ''' Parameters: board - type: Board object

            rotates the shape:
            1. Get the rotation direction using the get_rotation_dir method
            2. Compute the position of each block after rotation
            3. Move the block to the new position

        '''
        direction = self.get_rotation_dir()
        centre = self.blocks[1]
        for block in self.blocks:
            old_x = block.x
            old_y = block.y
            # print block, 'Old Co-ordinates:', old_x, old_y
            x = centre.x-direction*centre.y+direction*block.y
            y = centre.y+direction*centre.x-direction*block.x
            # print 'HAHA Co-ordinates:', x, '   ', y
            # print 'Self Co-ordinates:', block.x,'   ', block.y
            # Rectangle.__init__(block, block.x, block.y)
            block.move(x-block.x,y-block.y)

        ### This should be at the END of your rotate code.
        ### DO NOT touch it. Default behavior is that a piece will only shift
        ### rotation direciton after a successful rotation. This ensures that
        ### pieces which switch rotations definitely remain within their
        ### accepted rotation positions.
        if self.shift_rotation_dir:
            self.rotation_dir *= -1


############################################################
# ALL SHAPE CLASSES
############################################################
class I_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 2, center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y)]
        Shape.__init__(self, coords, 'blue')
        self.shift_rotation_dir = True
        self.center_block = self.blocks[2]


class J_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'orange')
        self.center_block = self.blocks[1]


class L_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'cyan')
        self.center_block = self.blocks[1]


class O_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x - 1, center.y),
                  Point(center.x   , center.y + 1),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'red')
        self.center_block = self.blocks[0]

    def rotate(self, board):
        # Override Shape's rotate method since O_Shape does not rotate
        return


class S_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y),
                  Point(center.x - 1, center.y + 1)]
        Shape.__init__(self, coords, 'green')
        self.center_block = self.blocks[0]
        self.shift_rotation_dir = True
        self.rotation_dir = -1


class T_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x + 1, center.y),
                  Point(center.x    , center.y + 1)]
        Shape.__init__(self, coords, 'yellow')
        self.center_block = self.blocks[1]


class Z_shape(Shape):
    def __init__(self, center):
        coords = [Point(center.x - 1, center.y),
                  Point(center.x    , center.y),
                  Point(center.x    , center.y + 1),
                  Point(center.x + 1, center.y + 1)]
        Shape.__init__(self, coords, 'magenta')
        self.center_block = self.blocks[1]
        self.shift_rotation_dir = True
        self.rotation_dir = -1


############################################################
# SCOREBOARD CLASS
############################################################
class ScoreBoard():

        preview_blocks = []   # class variable for storing blocks of previous preview

        def __init__(self, win, width, height):
            self.width = width
            self.height = height
            self.your_score = 0
            self.level = 1
            # create a canvas to draw the score on
            self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE/7)   # using 7 instead of 10
            self.canvas.setBackground('light green')

            self.msg0 = Text(Point(210,10), "Next Block")
            self.msg0.setFace('times roman')
            self.msg0.setStyle('bold')
            self.msg0.setSize(10)
            self.msg0.draw(self.canvas)
            self.msg2 = Text(Point(60,70), "Press P/p to pause")
            self.msg2.setFace('times roman')
            self.msg2.setStyle('bold')
            self.msg2.setSize(10)
            self.msg2.draw(self.canvas)

            self.msg = Text(Point(60, 10), "Your Score: " + str(self.your_score))
            self.lvl_msg = Text(Point(60, 30), "Your Level: " + str(self.level))
            self.get_score()
            # self.msg.setFace('times roman')
            # self.msg.setStyle('bold')
            # self.msg.setSize(10)
            # self.msg.draw(self.canvas)
            f2 = open('highscore.txt', 'a+')
            self.old_high_score = f2.read()
            f2.close()
            self.msg1 = Text(Point(60, 50), "High Score: " + str(self.old_high_score))
            # self.getHighScore()
            self.msg1.setFace('times roman')
            self.msg1.setStyle('bold')
            self.msg1.setSize(10)
            self.msg1.draw(self.canvas)

        def set_score(self):
            self.your_score += 1
            # print 'New score:', self.your_score
            if self.your_score >= 0 and self.your_score < 25:
                self.new_delay = 975
                self.level = 1
            elif self.your_score >= 25 and self.your_score < 50:
                self.new_delay = 950
                self.level = 2
            elif self.your_score >= 50 and self.your_score < 100:
                self.new_delay = 900
                self.level = 3
            elif self.your_score >= 100 and self.your_score < 150:
                self.new_delay=850
                self.level=4
            elif self.your_score >= 150 and self.your_score < 200:
                self.new_delay = 750
                self.level = 5
            else:
                self.new_delay = 500
                self.level = 6
            return self.new_delay

        def get_score(self):
            # print 'New score:', self.your_score
            self.msg.undraw()
            self.lvl_msg.undraw()
            # a.undraw()

            self.msg = Text(Point(60, 10), "Your Score: " + str(self.your_score))
            self.msg.setFace('times roman')
            self.msg.setStyle('bold')
            self.msg.setSize(10)
            self.msg.draw(self.canvas)
            self.lvl_msg = Text(Point(60, 30), "Your Level: " + str(self.level))
            self.lvl_msg.setFace('times roman')
            self.lvl_msg.setStyle('bold')
            self.lvl_msg.setSize(10)
            self.lvl_msg.draw(self.canvas)

        def set_high_score(self):
                # print'a:', a
                # print 'old_high_score:', self.old_high_score
                # strr = 200
                b = self.old_high_score
                if len(self.old_high_score) == 0:
                    b = 0

                if self.your_score >= int(b):
                    # print 'New High Score:', self.your_score

                    f1 = open('highscore.txt', 'w')
                    f1.write(str(self.your_score))
                    # print "printing write value:", f
                    # print f1.read()
                    f1.close()
                # else:
                    # print 'Not a high score'

        def draw_shape(self, shape):
            ''' Parameters: shape - type: Shape
                draws the shape on the board if there is space for it
                and returns True, otherwise it returns False
            '''
            # if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            # print 'Drawing Preview'
            for block in ScoreBoard.preview_blocks:
                block.undraw()
                # print 'undrawing'
            # shape.draw(self.canvas)

        @staticmethod
        def undraw_shape(shape):
            ScoreBoard.preview_blocks = shape.blocks


############################################################
# BOARD CLASS
############################################################
class Board():
    ''' Board class: it represents the Tetris board

        Attributes: width - type:int - width of the board in squares
                    height - type:int - height of the board in squares
                    canvas - type:CanvasFrame - where the pieces will be drawn
                    grid - type:Dictionary - keeps track of the current state of
                    the board; stores the blocks for a given position
    '''
    new_delay = 1000

    def __init__(self, win, width, height):
        self.width = width
        self.height = height

        # create a canvas to draw the tetris shapes on
        self.canvas = CanvasFrame(win, self.width * Block.BLOCK_SIZE,
                                        self.height * Block.BLOCK_SIZE)
        self.canvas.setBackground('light gray')

        # create an empty dictionary
        # currently we have no shapes on the board
        self.grid = {}

    def draw_shape(self, shape):
        ''' Parameters: shape - type: Shape
            Return value: type: bool

            draws the shape on the board if there is space for it
            and returns True, otherwise it returns False
        '''
        if shape.can_move(self, 0, 0):
            shape.draw(self.canvas)
            return True
        return False

    def can_move(self, x, y):
        ''' Parameters: x - type:int
                        y - type:int
            Return value: type: bool

            1. check if it is ok to move to square x,y
            if the position is outside of the board boundaries, can't move there
            return False

            2. if there is already a block at that postion, can't move there
            return False

            3. otherwise return True

        '''
        # print 'Grid:', self.grid
        if x < 0 or x > 9 or y < 0 or y > 19:
            return False
        elif (x,y) in self.grid:
            return False
        else:
            return True

    def add_shape(self, shape):
        ''' Parameter: shape - type:Shape

            add a shape to the grid, i.e.

            add each block to the grid using its
            (x, y) coordinates as a dictionary key

            Hint: use the get_blocks method on Shape to
            get the list of blocks

        '''
        # print shape.get_blocks()
        for block in shape.get_blocks():
            self.grid[block.x,block.y]=block
        # print 'printing grid:', self.grid

    def delete_row(self, y):
        ''' Parameters: y - type:int

            remove all the blocks in row y
            to remove a block you must remove it from the grid
            and erase it from the screen.
            If you dont remember how to erase a graphics object
            from the screen, take a look at the Graphics Library
            handout

        '''
        for x in range(0, self.width):
            row_block = self.grid.pop((x, y))
            # print 'row completed is:', row_block
            row_block.undraw()

    def is_row_complete(self, y):
        ''' Parameter: y - type: int
            Return value: type: bool

            for each block in row y
            check if there is a block in the grid (use the in operator)
            if there is one square that is not occupied, return False
            otherwise return True

        '''
        for x in range(0, self.width):
            row_block = (x,y) in self.grid
            if row_block:
                continue
            else:
                break
        return row_block

    def move_down_rows(self, y_start):
        ''' Parameters: y_start - type:int

            for each row from y_start to the top
                for each column
                    check if there is a block in the grid
                    if there is, remove it from the grid
                    and move the block object down on the screen
                    and then place it back in the grid in the new position

        '''
        for y1 in range (y_start, -1, -1):
            for x in range(0, self.width):
                 row_block = (x,y1) in self.grid
                 if row_block:
                     removed_block = self.grid.pop((x, y1))
                     removed_block.move(0,  1)
                     self.grid[(x, y1+1)] = removed_block

    def remove_complete_rows(self, scoreboard):
        ''' removes all the complete rows
            1. for each row, y,
            2. check if the row is complete
                if it is,
                    delete the row
                    move all rows down starting at row y - 1

        '''
        for y in range(0, self.height):
            if self.is_row_complete(y):
                self.delete_row(y)
                self.move_down_rows(y-1)

                Board.new_delay = scoreboard.set_score()    # setting the level of game
                scoreboard.get_score()

    def game_over(self, scoreboard):
        ''' display "Game Over !!!" message in the center of the board
            HINT: use the Text class from the graphics library
        '''
        msg = Text(Point(150, 200), "Game Over")
        msg.setFace('times roman')
        msg.setStyle('bold')
        msg.setSize(40)
        msg.draw(self.canvas)
        scoreboard.set_high_score()

    def pause(self, pause):
        '''self.msg11=Text(Point(150, 200)," Paused")
        self.msg11.setFace('times roman')
        self.msg11.setStyle('bold')
        self.msg11.setSize(40)'''

        if pause%2 == 1:
            self.msg11 = Text(Point(150, 200), "Game Paused\nPress P/p to resume")
            self.msg11.setFace('times roman')
            self.msg11.setStyle('bold')
            self.msg11.setSize(20)
            self.msg11.draw(self.canvas)
            # print 'paused'
        else:
            self.msg11.undraw()
            # print 'running'


############################################################
# TETRIS CLASS
############################################################
class Tetris():
    ''' Tetris class: Controls the game play
        Attributes:
            SHAPES - type: list (list of Shape classes)
            DIRECTION - type: dictionary - converts string direction to (dx, dy)
            BOARD_WIDTH - type:int - the width of the board
            BOARD_HEIGHT - type:int - the height of the board
            board - type:Board - the tetris board
            win - type:Window - the window for the tetris game
            delay - type:int - the speed in milliseconds for moving the shapes
            current_shapes - type: Shape - the current moving shape on the board
    '''

    SHAPES = [I_shape, J_shape, L_shape, O_shape, S_shape, T_shape, Z_shape]
    DIRECTION = {'Left':Point(-1, 0), 'Right':Point(1, 0), 'Down':Point(0, 1)}
    BOARD_WIDTH = 10
    BOARD_HEIGHT = 20
    b = random.randint(0, 6)   # O_shape(Point(int(BOARD_WIDTH/2),0))
    pause = 2

    def __init__(self, win):
        self.board = Board(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.scoreboard = ScoreBoard(win, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        self.win = win
        self.delay = 1000   # delay is in ms

        # sets up the keyboard events
        # when a key is called the method key_pressed will be called
        self.win.bind_all('<Key>', self.key_pressed)

        # set the current shape to a random new shape
        self.current_shape = self.create_new_shape()

        # Draw the current_shape oan the board (take a look at the
        # draw_shape method in the Board class)
        self.board.draw_shape(self.current_shape)

        # For Step 9:  animate the shape!
        self.animate_shape()

    def create_new_shape(self):
        ''' Return value: type: Shape

            Create a random new shape that is centered
             at y = 0 and x = int(self.BOARD_WIDTH/2)
            return the shape
        '''
        # return self.SHAPES[random.randint(0,6)](Point(int(self.BOARD_WIDTH/2),0))

        a = random.randint(0, 6)
        # b = self.SHAPES[a](Point(int(self.BOARD_WIDTH/2), 0))
        d = self.SHAPES[a](Point(int(self.BOARD_WIDTH/1.3), 0.7))
        self.scoreboard.draw_shape(d)
        self.scoreboard.undraw_shape(d)

        c = self.SHAPES[Tetris.b](Point(int(self.BOARD_WIDTH/2), 0))
        Tetris.b = a  # self.SHAPES[a](Point(int(self.BOARD_WIDTH/2), 0))
        return c

    def animate_shape(self):
        ''' animate the shape - move down at equal intervals
            specified by the delay attribute
        '''
        if Tetris.pause%2 == 0:
            self.do_move('Down')
        self.delay = Board.new_delay
        self.win.after(self.delay, self.animate_shape)

    def do_move(self, direction):
        ''' Parameters: direction - type: string
            Return value: type: bool

            Move the current shape in the direction specified by the parameter:
            First check if the shape can move. If it can, move it and return True
            Otherwise if the direction we tried to move was 'Down',
            1. add the current shape to the board
            2. remove the completed rows if any
            3. create a new random shape and set current_shape attribute
            4. If the shape cannot be drawn on the board, display a
               game over message

            return False

        '''
        # print self.DIRECTION[direction]
        a = self.DIRECTION[direction]
        b = self.current_shape.can_move(self.board, a.x, a.y)
        # print 'Printing b:', b
        if b:
            self.current_shape.move(a.x, a.y)
            return True
        else:
            if direction == 'Down':
                self.board.add_shape(self.current_shape)
                self.board.remove_complete_rows(self.scoreboard)
                # self.scoreboard.set_high_score()
                self.current_shape = self.create_new_shape()
                if self.board.draw_shape(self.current_shape):
                    pass
                else:
                    self.board.game_over(self.scoreboard)
            return False

    def do_rotate(self):
        ''' Checks if the current_shape can be rotated and
            rotates if it can
        '''
        a = self.current_shape.can_rotate(self.board)
        # print 'Upper Upper:',a
        if a:
            self.current_shape.rotate(self.board)

    def key_pressed(self, event):
        ''' this function is called when a key is pressed on the keyboard
            it currently just prints the value of the key

            Modify the function so that if the user presses the arrow keys
            'Left', 'Right' or 'Down', the current_shape will move in
            the appropriate direction

            if the user presses the space bar 'space', the shape will move
            down until it can no longer move and is added to the board

            if the user presses the 'Up' arrow key ,
                the shape should rotate.

        '''
        key = event.keysym
        # print key
        if Tetris.pause%2 == 0:
            if key == 'Left' or key == 'Right' or key == 'Down':
                self.do_move(key)
            elif key == 'space':
                bool = True
                while bool:
                    bool = self.do_move('Down')
            elif key == 'Up':
                self.do_rotate()
        else:
            pass
        if key == 'P' or key == 'p':
            Tetris.pause += 1
            # print 'pause:', Tetris.pause
            self.board.pause(Tetris.pause)
        else:
            pass

################################################################
# Start the game
################################################################

win = Window("Tetris")
game = Tetris(win)
win.mainloop()