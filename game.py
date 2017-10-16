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
        out = '   '
        for j in range(self.width):
            out += str(j + 1) + ' '
        out += '\n'
        for i in range(self.height):
            out += '\n'
            out += str(i + 1) + '  '
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
        return sum([x.count(REPRESENTATION[0]) for x in self.data])

    def countPlayerO(self):
        return sum([x.count(REPRESENTATION[1]) for x in self.data])

    def countEmptySpace(self):
        return sum([x.count(REPRESENTATION[2]) for x in self.data])

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

    def play(self):
        """
        Play the game.
        """
        endOfGame = False
        while not endOfGame:
            if self.moveNow == 'user':
                success = False
                while not success:
                    init, dest = self.getMove()
                    success = self.makeMove(init, dest, int(self.moveNow==self.moveFirst))
                self.moveNow = 'computer'
            else:
                currentState = GameState(self.grid, None, 'computer', 1, float('-inf'))
                bestValue, move = agent.minmax(currentState)
                self.moveNow = 'user'
            print grid
            endOfGame = self.checkEndOfGame(int(self.moveNow==self.moveFirst))
        if self.moveNow == 'computer':
            print 'Congratulations! You win!'
        else:
            print 'Oops... You lose.'

    def getMove(self):
        """
        Get the move of the user from keyboard.
        """
        init = tuple(int(str.strip()) for str in raw_input('Choose your initial position: ').split(','))
        while (len(init) != 2) or (init[0] not in range(1, self.grid.width+1)) or (init[1] not in range(1, self.grid.height+1)):
            print 'Initial position is not valid.'
            init = tuple(int(str.strip()) for str in raw_input('Choose your initial position: ').split(','))

        dest = tuple(int(str.strip()) for str in raw_input('Choose your destination: ').split(','))
        while (len(dest) != 2) or (dest[0] not in range(1, self.grid.width+1)) or (dest[1] not in range(1, self.grid.height+1)):
            print 'Destination position is not valid.'
            dest = tuple(int(str.strip()) for str in raw_input('Choose your destination: ').split(','))

        return (init, dest)

    def makeMove(self, initialPosition, destinationPosition, colorIndex):
        """
        Make move given by getMove().Assume input tuples are in the range of 
        board(checked in getMove().
        :param initialPosition: a tuple of coordinate (x,y)
        :param destinationPosition: a tuple of coordinate (x,y)
        :param colorIndex: the index of the color being moved now
        :return: True or False
        """
        checkColor = self.grid.REPRESENTATION[colorIndex]
        otherColor = self.grid.REPRESENTATION[1-colorIndex]
        emptyColor = self.grid.REPRESENTATION[2]
        if self.grid[initialPosition] != checkColor:  # initial position does not have the correct color
            print 'The piece you are trying to move is not yours! Please reselect your move.'
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
                # check legal move along the way
                for i in range(initialPosition[1]+1, destinationPosition[1], 2):
                    if self.grid[(x, i)] != otherColor and self.grid[(x, i+1)] != emptyColor:
                    print 'Invalid move! Please reselect your move.'
                    return False
                # change the grid
                self.grid[initialPosition], self.grid[destinationPosition] = ".", checkColor
                for i in range(initialPosition[1]+1, destinationPosition[1], 2):
                    self.grid[(x, i)] = emptyColor
                return True
            else:
                # check legal move along the way
                for i in range(initialPosition[1]-1, destinationPosition[1], -2):
                    if self.grid[(x, i)] != otherColor and self.grid[(x, i-1)] != emptyColor:
                    print 'Invalid move! Please reselect your move.'
                    return False
                # change the grid
                self.grid[initialPosition], self.grid[destinationPosition] = ".", checkColor
                for i in range(initialPosition[1]-1, destinationPosition[1], -2):
                    self.grid[(x, i)] = emptyColor
                return True
        elif initialPosition[1] == destinationPosition[1]:
            y = initialPosition[1]
            if (destinationPosition[0] - initialPosition[0]) %2 != 0:
                print 'Invalid move! Please reselect your move.'
                return False
            if initialPosition[0] < destinationPosition[0]:
                # check legal move along the way
                for i in range(initialPosition[0]+1, destinationPosition[0], 2):
                    if self.grid[(i, y)] != otherColor and self.grid[(i+1, y)] != emptyColor:
                    print 'Invalid move! Please reselect your move.'
                    return False
                # change the grid
                self.grid[initialPosition], self.grid[destinationPosition] = ".", checkColor
                for i in range(initialPosition[0]+1, destinationPosition[0], 2):
                    self.grid[(i, y)] = emptyColor
                return True
            else:
                # check legal move along the way
                for i in range(initialPosition[0]-1, destinationPosition[0], -2):
                    if self.grid[(i, y)] != otherColor and self.grid[(i-1, y)] != emptyColor:
                    print 'Invalid move! Please reselect your move.'
                    return False
                # change the grid
                self.grid[initialPosition], self.grid[destinationPosition] = ".", checkColor
                for i in range(initialPosition[0]-1, destinationPosition[0], -2):
                    self.grid[(i, y)] = emptyColor
                return True
        # make turns
        print 'Invalid move! Please reselect your move.'
        return False


    def checkEndOfGame(self, colorIndex):
        """
        Check if it's the end of game.
        :param colorIndex: the index of the color being moved now
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

    def __init__(self, grid, move, player, level, bestValue):
        self.grid = grid.copy()
        self.move = move
        self.player = player
        self.level = level
        self.bestValue = bestValue
