from agent import minimaxNaive
from agent import minimaxAlphaBeta
from agent import randomAgent
from agent import MinimaxInfo

class Grid:
    """
    A 2-dimensional array which represents the board of Konone.
    """

    def __init__(self, width=8, height=8):
        """
        :param width: width of the game board
        :param height: height of the game board
        """
        self.REPRESENTATION = ['X', 'O', '.']

        self.width = width
        self.height = height
        self.data = [[self.REPRESENTATION[(x + y) % 2] for y in range(height)] for x in range(width)]

    def __getitem__(self, index):
        """
        Get an item from the game board.
        :param index: index of the cell in the game board represented by a 2-tuple
        :return the value of the cell
        """
        return self.data[index[0] - 1][index[1] - 1]

    def __setitem__(self, index, item):
        """
        Set an item in the game board.
        :param index: index of the cell in the game board represented by a 2-tuple
        :param item: the expected value of the cell in the game board
        """
        if item not in self.REPRESENTATION: raise Exception('Grids can only \'X\', \'O\' and \'.\'')
        self.data[index[0] - 1][index[1] - 1] = item

    def __str__(self):
        """
        Represent the game board by a string.
        :return the string representation of the board
        """
        out = '    '
        for j in range(self.width):
            out += str(j + 1) + ' '
        out += '\n'
        for i in range(self.height):
            out += '\n'
            out += str(i + 1) + '   '
            for j in range(self.width):
                out += self.data[i][j] + ' '
        return out

    def __eq__(self, other):
        """
        Compare two game boards.
        :param other: the other board being compared
        :return if the two boards are the same
        """
        if other == None: return False
        return self.data == other.data

    def __hash__(self):
        """
        The hash function of the game board.
        :return the hash value of the game board
        """
        base = 1
        h = 0
        for l in self.data:
            for i in l:
                if i:
                    h += base
                base *= 2
        return hash(h)

    def copy(self):
        """
        :return a deep copy of the game board
        """
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        """
        :return a deep copy of the game board
        """
        return self.copy()

    def shallowCopy(self):
        """
        :return a shallow copy of the game board
        """
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def countPlayerX(self):
        """
        :return the total number of dark pieces on the board
        """
        return sum([x.count(self.REPRESENTATION[0]) for x in self.data])

    def countPlayerO(self):
        """
        :return the total number of light pieces on the board
        """
        return sum([x.count(self.REPRESENTATION[1]) for x in self.data])

    def countPlayerXEdge(self):
        """
        :return the total number of dark pieces on the edge of the board
        """
        result = self.data[0].count(self.REPRESENTATION[0]) + self.data[height-1].count(self.REPRESENTATION[0])
        for x in range(1, height-1):
            if self.data[x][0] == self.REPRESENTATION[0]:
                result += 1
        return result

    def countPlayerYEdge(self):
        """
        :return the total number of light pieces on the edge of the board
        """
        result = self.data[0].count(self.REPRESENTATION[1]) + self.data[height-1].count(self.REPRESENTATION[1])
        for x in range(1, height-1):
            if self.data[x][0] == self.REPRESENTATION[1]:
                result += 1
        return result

    def countEmptySpace(self):
        """
        :return the total number of empty cells on the board
        """
        return sum([x.count(self.REPRESENTATION[2]) for x in self.data])

    def asList(self):
        """
        :return the 2D game board as a 1D list
        """
        list = []
        for x in range(self.width):
            for y in range(self.height):
                list.append((x, y))
        return list


class Game:
    """
    Play the Konane game.
    """

    def __init__(self, moveFirst, width=8, height=8):
        """
        :param width: width of the game board
        :param height: height of the game board
        """
        if moveFirst not in ['computer', 'user']:
            raise Exception('Either computer or user move first.')
        self.moveFirst = moveFirst
        self.moveNow = moveFirst
        self.grid = Grid(width, height)

    def play(self, minimaxDepth, ifPrint, ifTestRandom, ifTestCombat, ifAlphaBeta):
        """
        Play the game.
        :param minimaxDepth: an integer represents the depth of the minimax search
        :param ifPrint: a boolean represents if the board information of each step is printed
        :param ifTestRandom: a boolean represents whether to let a random agent play as the user to test
        :param ifTestCombat: a boolean represents whether to let a minimax agent play as the user to test
        :param ifAlphaBeta: a boolean represents whether to use alpha beta pruning in the minimax algorithm
        :return 1 if the player wins, 0 if the computer wins
        """
        round = 1
        endOfGame = False
        firstMove = ()

        userMinimaxInfo = MinimaxInfo()
        computerMinimaxInfo = MinimaxInfo()
        while not endOfGame:
            if ifPrint:
                print self.grid
            if self.moveNow == 'user':
                if ifTestCombat:
                    #test: two minimax agents combat with each other
                    if round == 1:
                        currentState = GameState(self.grid, None, 'user', int(self.moveNow!=self.moveFirst))
                        
                        firstMove = None
                        minimaxInfo = None
                        if ifAlphaBeta:
                            bestValue, firstMove, minimaxInfo = minimaxAlphaBeta(currentState, minimaxDepth, round, float('-inf'), float('inf'))
                        else:
                            bestValue, firstMove, minimaxInfo = minimaxNaive(currentState, minimaxDepth, round)
                        
                        userMinimaxInfo += minimaxInfo
                        self.grid[firstMove] = self.grid.REPRESENTATION[2]
                        if ifPrint:
                            print 'User removed piece at', firstMove

                    elif round == 2:
                        currentState = GameState(self.grid, None, 'user', int(self.moveNow!=self.moveFirst))
                        
                        secondMove = None
                        minimaxInfo = None
                        if ifAlphaBeta:
                            bestValue, secondMove, minimaxInfo = minimaxAlphaBeta(currentState, minimaxDepth, round, float('-inf'), float('inf'))
                        else:
                            bestValue, secondMove, minimaxInfo = minimaxNaive(currentState, minimaxDepth, round)
                        
                        userMinimaxInfo += minimaxInfo
                        self.grid[secondMove] = self.grid.REPRESENTATION[2]
                        if ifPrint:
                            print 'User removed piece at', secondMove
                    else:
                        currentState = GameState(self.grid, None, 'user', int(self.moveNow!=self.moveFirst))
                        
                        move = None
                        minimaxInfo = None
                        if ifAlphaBeta:
                            bestValue, move, minimaxInfo = minimaxAlphaBeta(currentState, minimaxDepth, round, float('-inf'), float('inf'))
                        else:
                            bestValue, move, minimaxInfo = minimaxNaive(currentState, minimaxDepth, round)
                        
                        userMinimaxInfo += minimaxInfo
                        self.makeMove(move[0], move[1], int(self.moveNow!=self.moveFirst))
                        if ifPrint:
                            print 'User moved piece at', move[0], 'to', move[1]
                elif ifTestRandom:
                    # test: a random agent combat with a minimax agent
                    currentState = GameState(self.grid, None, 'user', int(self.moveNow!=self.moveFirst))
                    move = randomAgent(currentState, round)
                    if round == 1 or round == 2:
                        self.grid[move] = self.grid.REPRESENTATION[2]
                    else:
                        self.makeMove(move[0], move[1], int(self.moveNow!=self.moveFirst))
                    if ifPrint:
                            print 'User moved piece at', move[0], 'to', move[1]
                else:
                    if round == 1:
                        firstMove = self.getFirstMove()
                        self.grid[firstMove] = self.grid.REPRESENTATION[2]
                    elif round == 2:
                        secondMove = self.getSecondMove(firstMove)
                        self.grid[secondMove] = self.grid.REPRESENTATION[2]
                    else:
                        success = False
                        while not success:
                            init, dest = self.getMove()
                            success = self.checkLegalMove(init, dest, int(self.moveNow!=self.moveFirst))
                        self.makeMove(init, dest, int(self.moveNow!=self.moveFirst))

                self.moveNow = 'computer'
            else:
                if round == 1:
                    currentState = GameState(self.grid, None, 'computer', int(self.moveNow!=self.moveFirst))     
                    
                    firstMove = None
                    minimaxInfo = None
                    if ifAlphaBeta:
                        bestValue, firstMove, minimaxInfo = minimaxAlphaBeta(currentState, minimaxDepth, round, float('-inf'), float('inf'))
                    else:
                        bestValue, firstMove, minimaxInfo = minimaxNaive(currentState, minimaxDepth, round)

                    computerMinimaxInfo +=  minimaxInfo
                    self.grid[firstMove] = self.grid.REPRESENTATION[2]
                    if ifPrint:
                        print 'Computer removed piece at', firstMove
                elif round == 2:
                    currentState = GameState(self.grid, None, 'computer', int(self.moveNow!=self.moveFirst))
                    
                    secondMove = None
                    minimaxInfo = None
                    if ifAlphaBeta:
                        bestValue, secondMove, minimaxInfo = minimaxAlphaBeta(currentState, minimaxDepth, round, float('-inf'), float('inf'))
                    else:
                        bestValue, secondMove, minimaxInfo = minimaxNaive(currentState, minimaxDepth, round)

                    computerMinimaxInfo +=  minimaxInfo
                    self.grid[secondMove] = self.grid.REPRESENTATION[2]
                    if ifPrint:
                        print 'Computer removed piece at', secondMove
                else:
                    currentState = GameState(self.grid, None, 'computer', int(self.moveNow!=self.moveFirst))
                    
                    move = None
                    minimaxInfo = None
                    if ifAlphaBeta:
                        bestValue, move, minimaxInfo = minimaxAlphaBeta(currentState, minimaxDepth, round, float('-inf'), float('inf'))
                    else:
                        bestValue, move, minimaxInfo = minimaxNaive(currentState, minimaxDepth, round)

                    computerMinimaxInfo +=  minimaxInfo
                    self.makeMove(move[0], move[1], int(self.moveNow!=self.moveFirst))
                    if ifPrint:
                        print 'Computer moved piece at', move[0], 'to', move[1]
                self.moveNow = 'user'
            if round > 2:
                endOfGame = self.checkEndOfGame(int(self.moveNow!=self.moveFirst))
            round += 1

        if ifPrint:
            print self.grid

        if ifTestCombat:
            print '\nUser minimax meta information:'
            print 'Total times of static evaluation:', userMinimaxInfo.numberEvaluation
            print 'Average branching factor:', userMinimaxInfo.totalBranchingFactors * 1.00 / userMinimaxInfo.numberBranchingFactors
            if ifAlphaBeta:
                print 'Number of cutoffs:', userMinimaxInfo.numberCutoffs

        print '\nComputer minimix meta information:'
        print 'Total times of static evaluation:', computerMinimaxInfo.numberEvaluation
        print 'Average branching factor:', computerMinimaxInfo.totalBranchingFactors * 1.00 / computerMinimaxInfo.numberBranchingFactors
        if ifAlphaBeta:
            print 'Number of cutoffs:', computerMinimaxInfo.numberCutoffs

        if self.moveNow == 'computer':
            print 'Congratulations! You win!'
            return 1
        else:
            print 'Oops... You lose.'
            return 0
            

    def getMove(self):
        """
        Get the move of the user from keyboard.
        :return: tuple of the initial and destination position
        """
        while True:
            try:
                init = tuple(int(str.strip()) for str in raw_input('Choose the initial position of your move: ').split(','))
                break
            except ValueError:
                print("Input is not integer.")

        while (len(init) != 2) or (init[0] not in range(1, self.grid.width+1)) or (init[1] not in range(1, self.grid.height+1)):
            print 'Initial position is not valid.'
            init = tuple(int(str.strip()) for str in raw_input('Choose the initial position of your move: ').split(','))

        while True:
            try:
                dest = tuple(int(str.strip()) for str in raw_input('Choose the destination position of your move: ').split(','))
                break
            except ValueError:
                print("Input is not integer.")

        while (len(dest) != 2) or (dest[0] not in range(1, self.grid.width+1)) or (dest[1] not in range(1, self.grid.height+1)):
            print 'Destination position is not valid.'
            dest = tuple(int(str.strip()) for str in raw_input('Choose the destination position of your move: ').split(','))

        return (init, dest)

    def getFirstMove(self):
        """
        Get the first move of the user from keyboard.
        :return: tuple of the piece position
        """
        while True:
            try:
                move = tuple(int(str.strip()) for str in raw_input('Choose your first move: ').split(','))
                break
            except ValueError:
                print("Input is not a integer.")

        while move not in [(1, 1), (self.grid.width/2, self.grid.height/2), \
                (self.grid.width/2+1, self.grid.height/2+1), (self.grid.width, self.grid.height)]:
            print 'First move is not valid.'
            move = tuple(int(str.strip()) for str in raw_input('Choose your first move: ').split(','))
        return move

    def getSecondMove(self, firstMove):
        """
        Get the second move of the user from keyboard.
        :return: tuple of the piece position
        """
        while True:
            try:
                move = tuple(int(str.strip()) for str in raw_input('Choose your second move: ').split(','))
                break
            except ValueError:
                print("Input is not a integer.")

        while len(move) != 2 or abs(move[0]-firstMove[0]) + abs(move[1]-firstMove[1]) != 1:
            print 'Second move is not valid.'
            move = tuple(int(str.strip()) for str in raw_input('Choose your second move: ').split(','))
        return move

    def checkLegalMove(self, initialPosition, destinationPosition, colorIndex):
        """
        Check if the move is legal. Assume initial and destination positions are in the range of board.
        :param initialPosition: a tuple of coordinate (x,y)
        :param destinationPosition: a tuple of coordinate (x,y)
        :param colorIndex: the index of the color being moved now in Grid.REPRESENTATION
        :return: True if the move is legal, False if it is not
        """
        checkColor = self.grid.REPRESENTATION[colorIndex]
        otherColor = self.grid.REPRESENTATION[1-colorIndex]
        emptyColor = self.grid.REPRESENTATION[2]
        if self.grid[initialPosition] != checkColor:
            print 'The piece you are trying to move is not yours! Please reselect your move.'
            return False
        if self.grid[destinationPosition] != emptyColor:
            print 'The destination position of your move is not empty! Please reselect your move.'
            return False
        if initialPosition == destinationPosition:
            print 'The initial and destination position of your move are the same. Please reselect your move.'
            return False

        if initialPosition[0] == destinationPosition[0]:
            x = initialPosition[0]
            if (destinationPosition[1] - initialPosition[1]) %2 != 0:
                print 'Invalid move! Please reselect your move.'
                return False
            if initialPosition[1] < destinationPosition[1]:
                for i in range(initialPosition[1]+1, destinationPosition[1], 2):
                    if self.grid[(x, i)] != otherColor or self.grid[(x, i+1)] != emptyColor:
                        print 'Invalid move! Please reselect your move.'
                        return False
                return True
            else:
                for i in range(initialPosition[1]-1, destinationPosition[1], -2):
                    if self.grid[(x, i)] != otherColor or self.grid[(x, i-1)] != emptyColor:
                        print 'Invalid move! Please reselect your move.'
                        return False
                return True
        elif initialPosition[1] == destinationPosition[1]:
            y = initialPosition[1]
            if (destinationPosition[0] - initialPosition[0])%2 != 0:
                print 'Invalid move! Please reselect your move.'
                return False
            if initialPosition[0] < destinationPosition[0]:
                for i in range(initialPosition[0]+1, destinationPosition[0], 2):
                    if self.grid[(i, y)] != otherColor or self.grid[(i+1, y)] != emptyColor:
                        print 'Invalid move! Please reselect your move.'
                        return False
                return True
            else:
                for i in range(initialPosition[0]-1, destinationPosition[0], -2):
                    if self.grid[(i, y)] != otherColor or self.grid[(i-1, y)] != emptyColor:
                        print 'Invalid move! Please reselect your move.'
                        return False
                return True
        # make turns
        print 'Making turns is invalid move! Please reselect your move.'
        return False

    def makeMove(self, initialPosition, destinationPosition, colorIndex):
        """
        Make move by changing the grid.
        :param initialPosition: a tuple of coordinate (x,y)
        :param destinationPosition: a tuple of coordinate (x,y)
        :param colorIndex: the index of the color being moved now in Grid.REPRESENTATION
        """
        checkColor = self.grid.REPRESENTATION[colorIndex]
        otherColor = self.grid.REPRESENTATION[1-colorIndex]
        emptyColor = self.grid.REPRESENTATION[2]

        self.grid[initialPosition], self.grid[destinationPosition] = ".", checkColor

        if initialPosition[0] == destinationPosition[0]:
            x = initialPosition[0]
            if initialPosition[1] < destinationPosition[1]:
                for i in range(initialPosition[1]+1, destinationPosition[1], 2):
                    self.grid[(x, i)] = emptyColor
            else:
                for i in range(initialPosition[1]-1, destinationPosition[1], -2):
                    self.grid[(x, i)] = emptyColor
        else:
            y = initialPosition[1]
            if initialPosition[0] < destinationPosition[0]:
                for i in range(initialPosition[0]+1, destinationPosition[0], 2):
                    self.grid[(i, y)] = emptyColor
            else:
                for i in range(initialPosition[0]-1, destinationPosition[0], -2):
                    self.grid[(i, y)] = emptyColor


    def checkEndOfGame(self, colorIndex):
        """
        Check if it's the end of game.
        :param colorIndex: the index of the color being moved now in Grid.REPRESENTATION
        :return: True if the game ends, False else
        """
        checkColor = self.grid.REPRESENTATION[colorIndex]
        otherColor = self.grid.REPRESENTATION[1-colorIndex]
        emptyColor = self.grid.REPRESENTATION[2]
        for i in range(1, self.grid.width+1):
            for j in range(1, self.grid.height+1):
                if self.grid[i, j] != checkColor:
                    continue
                if (i > 2) and (self.grid[i-1, j] == otherColor) and (self.grid[i-2, j] == emptyColor):
                    return False
                if (i < self.grid.width-1) and (self.grid[i+1, j] == otherColor) and (self.grid[i+2, j] == emptyColor):
                    return False
                if (j > 2) and (self.grid[i, j-1] == otherColor) and (self.grid[i, j-2] == emptyColor):
                    return False
                if (j < self.grid.height-1) and (self.grid[i, j+1] == otherColor) and (self.grid[i, j+2] == emptyColor):
                    return False
        return True


class GameState:
    """
    Store game state of Konone.
    """

    def __init__(self, grid, move, player, colorIndex):
        """
        :param grid: the current game board.
        :param move: a tupe of the initial and destination positions of the move
        :param player: the current player
        :param colorIndex: the piece color of the current player
        """
        self.grid = grid.copy()
        self.move = move
        self.player = player
        self.minMax = 'max' if player == 'computer' else 'min'
        self.colorIndex = colorIndex
        self.bestValue = None

    def copy(self):
        """
        :return a deep copy of the game state
        """
        return GameState(self.grid.deepCopy(), self.move, self.player, self.colorIndex, self.bestValue)

    def deepCopy(self):
        """
        :return a deep copy of the game state
        """
        return self.copy()

    def evaluate(self):
        """
        Calculate the evaluation score for current state.
        :param grid: the current game board
        :return: the evaluation value of the grid for checkColor
        """
        # if player has no move, then player lost, -inf or inf depend on who the player is
        # if player has moves, use heuristics.
        
        #checkColorMoves = self.getAvailableMoves(self.colorIndex)
        #otherColorMoves = self.getAvailableMoves(1-self.colorIndex)
        
        checkColorMoves = self.getAvailableMovesPreferLonger(self.colorIndex)
        otherColorMoves = self.getAvailableMovesPreferLonger(1-self.colorIndex)

        checkColorPieces = self.getPieceCount(self.colorIndex)
        otherColorPieces = self.getPieceCount(1-self.colorIndex)

        #checkColorEdgePieces = self.getEgdePieceCount(self.colorIndex)
        #otherColorEdgePieces = self.getEgdePieceCount(1-self.colorIndex)

        if self.player == 'computer':
            if checkColorMoves == 0: #computer doesn't have moves
                return float('-inf')
            elif otherColorMoves == 0: #user doesn't have moves
                return float('inf')
            else:
                #return checkColorPieces - otherColorPieces
                return checkColorMoves - otherColorMoves
        else:
            if checkColorMoves == 0: #user doesn't have moves
                return float('inf')
            elif otherColorMoves == 0: #computer doesn't have moves
                return float('-inf')
            else:
                #return otherColorPieces - checkColorPieces
                return otherColorMoves - checkColorMoves

    def getPieceCount(self, checkColorIndex):
        """
        Calculate the numbers of pieces of a certain color
        :param checkColorIndex: the index of color of the player being checked
        :return: the number of pieces of a certain color
        """
        return self.grid.countPlayerX() if self.grid.REPRESENTATION[checkColorIndex] == 'X' \
            else self.grid.countPlayerO()

    def getEgdePieceCount(self, checkColorIndex):
        """
        Calculate the numbers of pieces on the edge of a certain color
        :param checkColorIndex: the index of color of the player being checked
        :return: the number of pieces on the edge of a certain color
        """
        return self.grid.countPlayerXEdge() if self.grid.REPRESENTATION[checkColorIndex] == 'X' \
            else self.grid.countPlayerOEdge()

    def getAvailableMoves(self, checkColorIndex):
        """
        Calculate the number of potential moves of a player. Moves that lie on the same direction
        are not repeatedly counted.
        :param checkColorIndex: the index of color of the player being checked
        :return: integer value of available moves for a certain color
        """
        checkColor = self.grid.REPRESENTATION[checkColorIndex]
        otherColor = self.grid.REPRESENTATION[1-checkColorIndex]
        emptyColor = self.grid.REPRESENTATION[2]

        result = 0
        for x in range(1, self.grid.width+1):
            for y in range(1, self.grid.height+1):
                if self.grid[x, y] != checkColor:
                    continue

                if x - 2 >= 1 and self.grid[x - 1, y] == otherColor \
                        and self.grid[x - 2, y] == emptyColor:
                    result += 1
                
                if x + 2 <= self.grid.width and self.grid[x + 1, y] == otherColor \
                        and self.grid[x + 2, y] == emptyColor:
                    result += 1

                if y - 2 >= 1 and self.grid[x, y - 1] == otherColor \
                        and self.grid[x, y - 2] == emptyColor:
                    result += 1

                if y + 2 <= self.grid.height and self.grid[x, y + 1] == otherColor \
                        and self.grid[x, y + 2] == emptyColor:
                    result += 1
        return result

    def getAvailableMovesPreferLonger(self, checkColorIndex):
        """
        Calculate the number of potential moves of a player. Moves that lie on the same direction
        are not repeatedly counted. Instead, the longer the player can move in one direction, the 
        higher score that direction will receive.
        :param checkColorIndex: the index of color of the player being checked
        :return: integer value of available moves for a certain color
        """
        checkColor = self.grid.REPRESENTATION[checkColorIndex]
        otherColor = self.grid.REPRESENTATION[1-checkColorIndex]
        emptyColor = self.grid.REPRESENTATION[2]

        result = 0
        for x in range(1, self.grid.width+1):
            for y in range(1, self.grid.height+1):
                if self.grid[x, y] != checkColor:
                    continue

                copy_x = x - 2
                while copy_x >= 1 and self.grid[copy_x+1, y] == otherColor \
                        and self.grid[copy_x, y] == emptyColor:
                    result += 1
                    copy_x -= 2
                
                copy_x = x + 2
                while copy_x <= self.grid.width \
                        and self.grid[copy_x-1, y] == otherColor \
                        and self.grid[copy_x, y] == emptyColor:
                    result += 1
                    copy_x += 2

                copy_y = y - 2
                while copy_y >= 1 and self.grid[x, copy_y+1] == otherColor \
                        and self.grid[x, copy_y] == emptyColor:
                    result += 1
                    copy_y -= 2

                copy_y = y + 2
                while copy_y <= self.grid.height \
                        and self.grid[x, copy_y-1] == otherColor \
                        and self.grid[x, copy_y] == emptyColor:
                    result += 1
                    copy_y += 2
        return result

    def getFirstMove(self):
        """
        :return the list of possible moves for the first move
        """
        emptyColor = self.grid.REPRESENTATION[2]
        listOfSuccessors = []
        otherPlayer = 'user' if self.player == 'computer' else 'computer'

        for (x, y) in [(1, 1), (self.grid.width/2, self.grid.height/2), \
                (self.grid.width/2+1, self.grid.height/2+1), (self.grid.width, self.grid.height)]:
            new_grid = self.grid.copy()
            new_grid[x, y] = emptyColor
            successor = GameState(new_grid, (x, y), otherPlayer, 1-self.colorIndex)
            listOfSuccessors.append(successor)
        return listOfSuccessors

    def getSecondMove(self):
        """
        :return the list of possible moves for the second move
        """
        checkColor = self.grid.REPRESENTATION[self.colorIndex]
        otherColor = self.grid.REPRESENTATION[1-self.colorIndex]
        emptyColor = self.grid.REPRESENTATION[2]

        listOfSuccessors = []
        listOfMoves = []
        otherPlayer = 'user' if self.player == 'computer' else 'computer'

        for x in range(1, self.grid.width+1):
            for y in range(1, self.grid.height+1):
                if self.grid[x, y] != checkColor:
                    continue

                if x-1 >= 1 and self.grid[x-1, y] == emptyColor:
                    listOfMoves.append((x, y))

                if x+1 <= self.grid.width and self.grid[x+1, y] == emptyColor:
                    listOfMoves.append((x, y))

                if y-1 >= 1 and self.grid[x, y-1] == emptyColor:
                    listOfMoves.append((x, y))

                if y+1 <= self.grid.height and self.grid[x, y+1] == emptyColor:
                    listOfMoves.append((x, y))

        for move in listOfMoves:
            new_grid = self.grid.copy()
            new_grid[move] = emptyColor
            successor = GameState(new_grid, move, otherPlayer, 1-self.colorIndex)
            listOfSuccessors.append(successor)
        return listOfSuccessors

    def getSuccessors(self):
        """
        :return the list of possible moves for any round of moves after the second round
        """
        checkColor = self.grid.REPRESENTATION[self.colorIndex]
        otherColor = self.grid.REPRESENTATION[1-self.colorIndex]
        emptyColor = self.grid.REPRESENTATION[2]

        listOfSuccessors = []
        otherPlayer = 'user' if self.player == 'computer' else 'computer'

        for x in range(1, self.grid.width+1):
            for y in range(1, self.grid.height+1):
                if self.grid[x, y] != checkColor:
                    continue

                new_grid = self.grid.copy()
                copy_x = x - 2
                while copy_x >= 1 \
                        and self.grid[copy_x+1, y] == otherColor \
                        and self.grid[copy_x, y] == emptyColor:
                    new_grid = new_grid.copy()
                    new_grid[copy_x+2, y] = emptyColor
                    new_grid[copy_x+1, y] = emptyColor
                    new_grid[copy_x, y] = checkColor
                    successor = GameState(new_grid, ((x, y), (copy_x, y)), 
                        otherPlayer, 1-self.colorIndex)
                    listOfSuccessors.append(successor)
                    copy_x -= 2

                new_grid = self.grid.copy()
                copy_x = x + 2
                while copy_x <= self.grid.width \
                        and self.grid[copy_x-1, y] == otherColor \
                        and self.grid[copy_x, y] == emptyColor:
                    new_grid = new_grid.copy()
                    new_grid[copy_x-2, y] = emptyColor
                    new_grid[copy_x-1, y] = emptyColor
                    new_grid[copy_x, y] = checkColor
                    successor = GameState(new_grid, ((x, y), (copy_x, y)), 
                        otherPlayer, 1-self.colorIndex)
                    listOfSuccessors.append(successor)
                    copy_x += 2

                new_grid = self.grid.copy()
                copy_y = y - 2
                while copy_y >= 1 \
                        and self.grid[x, copy_y+1] == otherColor \
                        and self.grid[x, copy_y] == emptyColor:
                    new_grid = new_grid.copy()
                    new_grid[x, copy_y+2] = emptyColor
                    new_grid[x, copy_y+1] = emptyColor
                    new_grid[x, copy_y] = checkColor
                    successor = GameState(new_grid, ((x, y), (x, copy_y)), 
                        otherPlayer, 1-self.colorIndex)
                    listOfSuccessors.append(successor)
                    copy_y -= 2

                new_grid = self.grid.copy()
                copy_y = y + 2
                while copy_y <= self.grid.height \
                        and self.grid[x, copy_y-1] == otherColor \
                        and self.grid[x, copy_y] == emptyColor:
                    new_grid = new_grid.copy()
                    new_grid[x, copy_y-2] = emptyColor
                    new_grid[x, copy_y-1] = emptyColor
                    new_grid[x, copy_y] = checkColor
                    successor = GameState(new_grid, ((x, y), (x, copy_y)), 
                        otherPlayer, 1-self.colorIndex)
                    listOfSuccessors.append(successor)
                    copy_y += 2

        return listOfSuccessors

def calculateWinRate():
    """
    Print the win rate of the user against the computer.
    """
    times = 10
    winRate = 0.0
    for i in range(times):
        game = Game('user', 6, 6)
        winRate += game.play(5, False, True, False, False)
    winRate = winRate/times
    print "Winrate:", winRate

game = Game('user', 6, 6)
game.play(5, True, False, False, True)

#calculateWinRate()