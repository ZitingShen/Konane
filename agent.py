import random

def minimaxNaive(state, limit, round):
    """
    Naive Minmax algorithm
    :param state: current state of game, class GameState
    :param limit: an integer that indicates limit
    :param round: the number of round
    :return: cbv, best move, minimax meta information
    """
    minimaxInfo = MinimaxInfo()

    if limit == 0:
        state.bestValue = state.evaluate()
        minimaxInfo.numberEvaluation += 1
        return state.bestValue, state.move, minimaxInfo

    listOfSuccessor = []
    if round == 1:
        listOfSuccessor = state.getFirstMove()
    elif round == 2:
        listOfSuccessor = state.getSecondMove()
    else:
        listOfSuccessor = state.getSuccessors()
    minimaxInfo.numberBranchingFactors += 1
    minimaxInfo.totalBranchingFactors += len(listOfSuccessor)

    if state.minMax == 'max':
        cbv = float("-inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move, successorMinimaxInfo = minimaxNaive(successor, limit-1, round+1)
            minimaxInfo += successorMinimaxInfo
            if bv > cbv:
                cbv = bv
                bestMove = successor.move
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove, minimaxInfo
    else:
        cbv = float("inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move, successorMinimaxInfo = minimaxNaive(successor, limit-1, round+1)
            minimaxInfo += successorMinimaxInfo
            if bv < cbv:
                cbv = bv
                bestMove = successor.move
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove, minimaxInfo


def minimaxAlphaBeta(state, limit, round, alpha, beta):
    """
    Minmax algorithm with Alpha-Beta pruning.
    :param state: current state of game, class GameState
    :param limit: an integer that indicates limit
    :param round: the number of round
    :param alpha: the min value of the max level
    :param beta: the max value of the min level
    :return: cbv, best move, minimax meta information
    """
    minimaxInfo = MinimaxInfo()

    if limit == 0:
        state.bestValue = state.evaluate()
        minimaxInfo.numberEvaluation += 1
        return state.bestValue, state.move, minimaxInfo

    listOfSuccessor = []
    if round == 1:
        listOfSuccessor = state.getFirstMove()
    elif round == 2:
        listOfSuccessor = state.getSecondMove()
    else:
        listOfSuccessor = state.getSuccessors()
    minimaxInfo.numberBranchingFactors += 1
    minimaxInfo.totalBranchingFactors += len(listOfSuccessor)

    if state.minMax == 'max':
        cbv = float("-inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move, successorMinimaxInfo = minimaxAlphaBeta(successor, limit-1, round+1, alpha, beta)
            minimaxInfo += successorMinimaxInfo
            if bv > cbv:
                cbv = bv
                bestMove = successor.move
                alpha = bv
            if beta <= alpha:
                minimaxInfo.numberCutoffs += 1
                break
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove, minimaxInfo
    else:
        cbv = float("inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move, successorMinimaxInfo = minimaxAlphaBeta(successor, limit-1, round+1, alpha, beta)
            minimaxInfo += successorMinimaxInfo
            if bv < cbv:
                cbv = bv
                bestMove = successor.move
                beta = bv
            if beta <= alpha:
                minimaxInfo.numberCutoffs += 1
                break
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove, minimaxInfo

def randomAgent(state, round):
    """
    An agent that randomly chooses a move among all current available moves.
    :param state: current state of game, class GameState
    :param round: the number of round
    :return: move chosen
    """
    listOfSuccessor = []
    if round == 1:
        listOfSuccessor = state.getFirstMove()
    elif round == 2:
        listOfSuccessor = state.getSecondMove()
    else:
        listOfSuccessor = state.getSuccessors()
    return random.choice(listOfSuccessor).move

class MinimaxInfo:
    """
    A class to store meta information used in the minimax algorithm.
    """
    def __init__(self, numberEvaluation=0, totalBranchingFactors=0, \
            numberBranchingFactors=0, numberCutoffs=0):
        """
        :param numberEvaluation: total number of evaluations
        :param totalBranchingFactors: total branching factors
        :param numberBranchingFactors: number of branching factors
        :param numberCutoffs: number of cutoffs
        """
        self.numberEvaluation = numberEvaluation
        self.totalBranchingFactors = totalBranchingFactors
        self.numberBranchingFactors = numberBranchingFactors
        self.numberCutoffs = numberCutoffs

    def __add__(self, other):
        """
        Add one MinimaxInfo object to another.
        :param other: the other MinimaxInfo object
        :return: the sum of the two MinimaxInfo objects
        """
        return MinimaxInfo(self.numberEvaluation + other.numberEvaluation, \
            self.totalBranchingFactors + other.totalBranchingFactors, \
            self.numberBranchingFactors + other.numberBranchingFactors, \
            self.numberCutoffs + other.numberCutoffs)


