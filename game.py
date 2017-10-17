import agent
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
        return self.data[index[1] - 1][index[0] - 1]

    def __setitem__(self, index, item):
        if item not in self.REPRESENTATION: raise Exception('Grids can only \'X\', \'O\' and \'.\'')
        self.data[index[1] - 1][index[0] - 1] = item

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
        self.round = 1

    def play(self):
        """
        Play the game.
        """
        endOfGame = False
        firstMove = ()
        while not endOfGame:
            print self.grid
            if self.round == 1:
                firstMove = self.getFirstMove()
                self.grid[firstMove] = self.grid.REPRESENTATION[2]
                if self.moveNow == 'user':
                    self.moveNow = 'computer'
                else:
                    self.moveNow = 'user'
                self.round += 1
            elif self.round == 2:
                secondMove = self.getSecondMove(firstMove)
                self.grid[secondMove] = self.grid.REPRESENTATION[2]
                if self.moveNow == 'user':
                    self.moveNow = 'computer'
                else:
                    self.moveNow = 'user'
                self.round += 1
            elif self.moveNow == 'user':
                success = False
                while not success:
                    init, dest = self.getMove()
                    success = self.makeMove(init, dest, 1-int(self.moveNow==self.moveFirst))
                self.moveNow = 'computer'
            else:
                currentState = GameState(self.grid, None, 'computer', 1, float('-inf'))
                bestValue, move = agent.minmax(currentState)
                self.moveNow = 'user'
            endOfGame = self.checkEndOfGame(int(self.moveNow==self.moveFirst))
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
        while move not in [(1, 1), (4, 4), (5, 5), (8, 8)]:
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
                # check legal move along the way
                for i in range(initialPosition[1]+1, destinationPosition[1], 2):
                    if self.grid[(x, i)] != otherColor or self.grid[(x, i+1)] != emptyColor:
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
                    if self.grid[(x, i)] != otherColor or self.grid[(x, i-1)] != emptyColor:
                        print 'Invalid move! Please reselect your move.'
                        return False
                # change the grid
                self.grid[initialPosition], self.grid[destinationPosition] = ".", checkColor
                for i in range(initialPosition[1]-1, destinationPosition[1], -2):
                    self.grid[(x, i)] = emptyColor
                return True
        elif initialPosition[1] == destinationPosition[1]:
            y = initialPosition[1]
            if (destinationPosition[0] - initialPosition[0])%2 != 0:
                print 'Invalid move! Please reselect your move.'
                return False
            if initialPosition[0] < destinationPosition[0]:
                # check legal move along the way
                for i in range(initialPosition[0]+1, destinationPosition[0], 2):
                    if self.grid[(i, y)] != otherColor or self.grid[(i+1, y)] != emptyColor:
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
                    if self.grid[(i, y)] != otherColor or self.grid[(i-1, y)] != emptyColor:
                        print 'Invalid move! Please reselect your move.'
                        return False
                # change the grid
                self.grid[initialPosition], self.grid[destinationPosition] = ".", checkColor
                for i in range(initialPosition[0]-1, destinationPosition[0], -2):
                    self.grid[(i, y)] = emptyColor
                return True
        # make turns
        print 'Making turns is invalid move! Please reselect your move.'
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


# game = Game('user', 4, 4)
# game.play()

class GameState:
    """
    Store game state of Konone.
    """

    def __init__(self, grid, move, player, level, bestValue, color):
        """
        :param grid:
        :param move: tuple of tuples ((x1, y1), (x2, y2))
        :param player:
        :param level:
        :param bestValue:
        :param color:
        """
        self.grid = grid.copy()
        self.move = move
        self.player = player
        self.level = level
        self.bestValue = bestValue
        self.minMax = "max" if self.player == "computer" else "min"
        self.color = color

    def copy(self):
        new_grid = self.grid.deepCopy()
        new_move = self.move
        new_player = self.player
        new_level = self.level
        new_bestValue = self.bestValue
        new_color = self.color
        s = GameState(new_grid, new_move, new_player, new_level, new_bestValue, new_color)
        return s

    def deepCopy(self):
        return self.copy()

    def evaluation(self, the_grid, colorOfComp):
        """
        :param the_grid:
        :param colorNow:
        :return:
        """
        # if player has no move, then player lost, -inf or inf depend on who the player is
        # if player has moves, use heuristics.
        colorOfUser = "X" if colorOfComp == "O" else "X"
        if getAvailableMoves(self, the_grid, "computer") == 0:
            return float("-inf")
        elif getAvailableMoves(self, the_grid, "user") == 0:
            return float("inf")
        else:
            return self.getAvailableMoves(the_grid, colorOfComp) - self.getAvailableMoves(the_grid. colorOfUser)

    def getAvailableMoves(self, the_grid, colorNow):
        """
        :param the_grid:
        :param player:
        :return: integer value of available moves for color
        """
        result = 0
        otherColor = "X" if colorNow == "O" else "X"
        emptyColor = "."
        for x in range(1, 9):
            for y in range(1, 9):
                if the_grid[x, y] == colorNow:
                    copy_x = x
                    while copy_x >= 3:
                        if the_grid[(copy_x - 1, y)] == otherColor and self.grid[(copy_x - 2, y)] == emptyColor:
                            result += 1
                            copy_x -= 2
                        else:
                            break
                    copy_x = x
                    while copy_x <= 6:
                        if the_grid[(copy_x + 1, y)] == otherColor and self.grid[(copy_x + 2, y)] == emptyColor:
                            result += 1
                            copy_x += 2
                        else:
                            break
                    copy_y = y
                    while copy_y >= 3:
                        if the_grid[(x, copy_y - 1)] == otherColor and self.grid[(x, copy_y - 2)] == emptyColor:
                            result += 1
                            copy_x -= 2
                        else:
                            break
                    copy_y = y
                    while copy_y <= 6:
                        if the_grid[(x, copy_y + 1)] == otherColor and self.grid[(x, copy_y + 2)] == emptyColor:
                            result += 1
                            copy_x += 2
                        else:
                            break
        return result

    def getSuccessors(self):
        listOfSuccessors = []
        colorNow = self.color
        otherColor = "X" if colorNow == "O" else "X"
        emptyColor = "."
        playerNow = self.player
        otherPlayer = "computer" if playerNow == "user" else "user"
        nextLevel = self.level + 1
        colorOfComp = colorNow if playerNow == "computer" else otherColor
        for x in range(1, 9):
            for y in range(1, 9):
                if self.grid[x, y] == colorNow:
                    copy_x = x
                    while copy_x >= 3:
                        if self.grid[(copy_x, y)] == colorNow and self.grid[(copy_x-1, y)] == otherColor \
                                and self.grid[(copy_x-2, y)] == emptyColor:
                            new_grid = self.grid.copy()
                            new_grid[(copy_x, y)] = emptyColor
                            new_grid[(copy_x-1), y] = emptyColor
                            new_grid[(copy_x-2), y] = colorNow
                            successor = GameState(new_grid, ((x, y), (copy_x-2, y)), otherPlayer, nextLevel,
                                                  self.evaluation(new_grid, colorOfComp), otherColor)
                            listOfSuccessors.append(successor)
                            copy_x -= 2
                        else:
                            break
                    copy_x = x
                    while copy_x+2 <= 6:
                        if self.grid[(copy_x, y)] == colorNow and self.grid[(copy_x+1, y)] == otherColor \
                                and self.grid[(copy_x+2, y)] == emptyColor:
                            new_grid = self.grid.copy()
                            new_grid[(copy_x, y)] = emptyColor
                            new_grid[(copy_x+1), y] = emptyColor
                            new_grid[(copy_x+2), y] = colorNow
                            successor = GameState(new_grid, ((x, y), (copy_x+2, y)), otherPlayer, nextLevel,
                                                  self.evaluation(new_grid, colorOfComp), otherColor)
                            listOfSuccessors.append(successor)
                            copy_x += 2
                        else:
                            break
                    copy_y = y
                    while copy_y >= 3:
                        if self.grid[(x, copy_y)] == colorNow and self.grid[(x,copy_y-1)] == otherColor \
                                and self.grid[(x, copy_y-2)] == emptyColor:
                            new_grid = self.grid.copy()
                            new_grid[(x, copy_y)] = emptyColor
                            new_grid[(x, copy_y-1)] = emptyColor
                            new_grid[(x, copy_y-2)] = colorNow
                            successor = GameState(new_grid, ((x, y), (x, copy_y-2)), otherPlayer, nextLevel,
                                                  self.evaluation(new_grid, colorOfComp), otherColor)
                            listOfSuccessors.append(successor)
                            copy_y -= 2
                        else:
                            break
                    copy_y = y
                    while copy_y <= 6:
                        if self.grid[(x, copy_y)] == colorNow and self.grid[(x,copy_y+1)] == otherColor \
                                and self.grid[(x, copy_y+2)] == emptyColor:
                            new_grid = self.grid.copy()
                            new_grid[(x, copy_y)] = emptyColor
                            new_grid[(x, copy_y+1)] = emptyColor
                            new_grid[(x, copy_y+2)] = colorNow
                            successor = GameState(new_grid, ((x, y), (x, copy_y+2)), otherPlayer, nextLevel,
                                                  self.evaluation(new_grid, colorOfComp), otherColor)
                            listOfSuccessors.append(successor)
                            copy_y += 2
                        else:
                            break
        return listOfSuccessors