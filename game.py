class Grid:
    """
    A 2-dimensional array which represents the board of Konone.
    """
    def __init__(self, width=8, height=8):
        self.REPRESENTATION = ['X', 'O', '.']

        self.width = width
        self.height = height
        self.data = [[self.REPRESENTATION[(x+y)%2] for y in range(height)] for x in range(width)]

    def __getitem__(self, index):
        return self.data[index[0]-1][index[1]-1]

    def __setitem__(self, index, item):
        if item not in self.REPRESENTATION: raise Exception('Grids can only \'X\', \'O\' and \'.\'')
        self.data[index[0]-1][index[1]-1] = item

    def __str__(self):
        out = '   '
        for j in range(self.width):
            out += str(j+1) + ' '
        out += '\n'
        for i in range(self.height):
            out += '\n'
            out += str(i+1) + '  '
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
                list.append((x,y))
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
        if self.moveNow == 'user':
            move = self.getMove()
            self.makeMove(move)
            self.moveNow == 'computer'
        else:
            currentState = GameState(self.grid, None, 'computer', 1, float('-inf'))
            bestValue, move = agent.minmax(currentState)
            self.moveNow = 'user'
        self.checkEndOfGame()

    def getMove(self):
        initialPos = raw_input('Choose')

    def makeMove(self, move):
        TODO

    def checkEndOfGame(self):
        TODO

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
