from agent import minimaxNaive
from agent import minimaxAlphaBeta

class Grid:
    """
    A 2-dimensional array which represents the board of Konone.
    """

    def __init__(self, width=8, height=8):
        self.REPRESENTATION = ['X', 'O', '.']

        self.width = width
        self.height = height
        self.data = [[self.REPRESENTATION[(x + y) % 2] for y in range(height)] for x in range(width)]

    def __getitem__(self, index):
        return self.data[index[0] - 1][index[1] - 1]

    def __setitem__(self, index, item):
        if item not in self.REPRESENTATION: raise Exception('Grids can only \'X\', \'O\' and \'.\'')
        self.data[index[0] - 1][index[1] - 1] = item

    def __str__(self):
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
        if other == None: return False
        return self.data == other.data

    def __hash__(self):
        # return hash(str(self))
        base = 1
        h = 0
        for l in self.data:
            for i in l:
                if i:
                    h += base
                base *= 2
        return hash(h)

    def copy(self):
        g = Grid(self.width, self.height)
        g.data = [x[:] for x in self.data]
        return g

    def deepCopy(self):
        return self.copy()

    def shallowCopy(self):
        g = Grid(self.width, self.height)
        g.data = self.data
        return g

    def countPlayerX(self):
        return sum([x.count(self.REPRESENTATION[0]) for x in self.data])

    def countPlayerO(self):
        return sum([x.count(self.REPRESENTATION[1]) for x in self.data])

    def countEmptySpace(self):
        return sum([x.count(self.REPRESENTATION[2]) for x in self.data])

    def asList(self):
        list = []
        for x in range(self.width):
            for y in range(self.height):
                list.append((x, y))
        return list


class Game:
    """
    Play the Konone game.
    """

    def __init__(self, moveFirst, width=8, height=8):
        if moveFirst not in ['computer', 'user']:
            raise Exception('Either computer or user move first.')
        self.moveFirst = moveFirst
        self.moveNow = moveFirst
        self.grid = Grid(width, height)

    def play(self, minimaxDepth):
        """
        Play the game.
        """
        round = 1
        endOfGame = False
        firstMove = ()
        while not endOfGame:
            print self.grid
            if self.moveNow == 'user':
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
                    bestValue, firstMove = minimaxNaive(currentState, minimaxDepth, round)
                    #bestValue, firstMove = minimaxAlphaBeta(currentState, minimaxDepth, round, float('-inf'), float('inf'))
                    self.grid[firstMove] = self.grid.REPRESENTATION[2]
                    print 'Computer removed piece at', firstMove, '.'
                elif round == 2:
                    currentState = GameState(self.grid, None, 'computer', int(self.moveNow!=self.moveFirst))
                    bestValue, secondMove = minimaxNaive(currentState, minimaxDepth, round)
                    #bestValue, secondMove = minimaxAlphaBeta(currentState, minimaxDepth, round, float('-inf'), float('inf'))
                    self.grid[secondMove] = self.grid.REPRESENTATION[2]
                    print 'Computer removed piece at', secondMove, '.'
                else:
                    currentState = GameState(self.grid, None, 'computer', int(self.moveNow!=self.moveFirst))
                    bestValue, move = minimaxNaive(currentState, minimaxDepth, round)
                    #bestValue, move = minimaxAlphaBeta(currentState, minimaxDepth, round, float('-inf'), float('inf'))
                    self.makeMove(move[0], move[1], int(self.moveNow!=self.moveFirst))
                    print 'Computer moved piece at', move[0], 'to', move[1], '.'
                self.moveNow = 'user'
            if round > 2:
                endOfGame = self.checkEndOfGame(int(self.moveNow!=self.moveFirst))
            round += 1

        print self.grid
        if self.moveNow == 'computer':
            print 'Congratulations! You win!'
        else:
            print 'Oops... You lose.'

    def getMove(self):
        """
        Get the move of the user from keyboard.
        :return: tuple of the initial and destination position
        """
        init = tuple(int(str.strip()) for str in raw_input('Choose the initial position of your move: ').split(','))
        while (len(init) != 2) or (init[0] not in range(1, self.grid.width+1)) or (init[1] not in range(1, self.grid.height+1)):
            print 'Initial position is not valid.'
            init = tuple(int(str.strip()) for str in raw_input('Choose the initial position of your move: ').split(','))

        dest = tuple(int(str.strip()) for str in raw_input('Choose the destination position of your move: ').split(','))
        while (len(dest) != 2) or (dest[0] not in range(1, self.grid.width+1)) or (dest[1] not in range(1, self.grid.height+1)):
            print 'Destination position is not valid.'
            dest = tuple(int(str.strip()) for str in raw_input('Choose the destination position of your move: ').split(','))

        return (init, dest)

    def getFirstMove(self):
        """
        Get the first move of the user from keyboard.
        :return: tuple of the piece position
        """
        move = tuple(int(str.strip()) for str in raw_input('Choose your first move: ').split(','))
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
        move = tuple(int(str.strip()) for str in raw_input('Choose your second move: ').split(','))
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
        :return: void
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
        :return: True or False
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

    def __init__(self, grid, move, player, colorIndex, bestValue=None):
        """
        :param grid: the current game board.
        :param move: a tupe of the initial and destination positions of the move
        :param player: the current player
        :param bestValue: the best evaluation value of levels below
        :param colorIndex: the piece color of the current player
        """
        self.grid = grid.copy()
        self.move = move
        self.player = player
        self.minMax = 'max' if self.player == 'computer' else 'min'
        self.colorIndex = colorIndex
        self.bestValue = self.evaluate() if bestValue == None else bestValue

    def copy(self):
        return GameState(self.grid.deepCopy(), self.move, self.player, self.colorIndex, self.bestValue)

    def deepCopy(self):
        return self.copy()

    def evaluate(self):
        """
        Calculate the evaluation score for current state.
        :param grid: the current game board
        :return: the evaluation value of the grid for checkColor
        """
        # if player has no move, then player lost, -inf or inf depend on who the player is
        # if player has moves, use heuristics.
        checkColorMoves = self.getAvailableMoves(self.colorIndex)
        otherColorMoves = self.getAvailableMoves(1-self.colorIndex)

        if self.player == 'computer':
            if checkColorMoves == 0: #computer doesn't have moves
                return float('-inf')
            elif otherColorMoves == 0: #user doesn't have moves
                return float('inf')
            else:
                return checkColorMoves - otherColorMoves
        else:
            if checkColorMoves == 0: #user doesn't have moves
                return float('inf')
            elif otherColorMoves == 0: #computer doesn't have moves
                return float('-inf')
            else:
                return otherColorMoves - checkColorMoves

    def getAvailableMoves(self, checkColorIndex):
        """
        Calculate the number of potential moves of a player. Moves that lie on the same direction
        are not repeatedly counted. Instead, the longer the player can move in one direction, the 
        higher score that direction will receive.
        :param grid: the current game board
        :param checkColorIndex: the index of color of the player being checked
        :return: integer value of available moves for color
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
        emptyColor = self.grid.REPRESENTATION[2]
        listOfSuccessors = []
        otherPlayer = 'user' if self.player == 'computer' else 'user'

        for (x, y) in [(1, 1), (self.grid.width/2, self.grid.height/2), \
                (self.grid.width/2+1, self.grid.height/2+1), (self.grid.width, self.grid.height)]:
            new_grid = self.grid.copy()
            new_grid[x, y] = emptyColor
            successor = GameState(new_grid, (x, y), otherPlayer, 1-self.colorIndex)
            listOfSuccessors.append(successor)
        return listOfSuccessors

    def getSecondMove(self):
        checkColor = self.grid.REPRESENTATION[self.colorIndex]
        otherColor = self.grid.REPRESENTATION[1-self.colorIndex]
        emptyColor = self.grid.REPRESENTATION[2]

        listOfSuccessors = []
        listOfMoves = []
        otherPlayer = 'user' if self.player == 'computer' else 'user'

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
        checkColor = self.grid.REPRESENTATION[self.colorIndex]
        otherColor = self.grid.REPRESENTATION[1-self.colorIndex]
        emptyColor = self.grid.REPRESENTATION[2]

        listOfSuccessors = []
        otherPlayer = 'user' if self.player == 'computer' else 'user'

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


game = Game('user')
game.play(4)