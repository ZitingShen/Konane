import random

def minimaxNaive(state, limit, round):
    """
    Naive Minmax algorithm
    :param state: current state of game, class GameState
    :param limit: an integer that indicates limit
    :return: cbv, best move
    """
    if limit == 0:
        return state.bestValue, state.move

    listOfSuccessor = []
    if round == 1:
        listOfSuccessor = state.getFirstMove()
    elif round == 2:
        listOfSuccessor = state.getSecondMove()
    else:
        listOfSuccessor = state.getSuccessors()

    if state.minMax == 'max':
        cbv = float("-inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move = minimaxNaive(successor, limit-1, round+1)
            if bv > cbv:
                cbv = bv
                bestMove = successor.move
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove
    else:
        cbv = float("inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move = minimaxNaive(successor, limit-1, round+1)
            if bv < cbv:
                cbv = bv
                bestMove = successor.move
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove


def minimaxAlphaBeta(state, limit, round, alpha, beta):
    """
    Minmax algorithm with Alpha-Beta pruning.
    :param state:
    :param alpha:
    :param beta:
    :return:
    """
    if limit == 0:
        return state.bestValue, state.move

    listOfSuccessor = []
    if round == 1:
        listOfSuccessor = state.getFirstMove()
    elif round == 2:
        listOfSuccessor = state.getSecondMove()
    else:
        listOfSuccessor = state.getSuccessors()

    if state.minMax == 'max':
        cbv = float("-inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move = minimaxAlphaBeta(successor, limit-1, round+1, alpha, beta)
            if bv > cbv:
                cbv = bv
                bestMove = successor.move
                alpha = bv
            if beta <= alpha:
                break
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove
    else:
        cbv = float("inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move = minimaxAlphaBeta(successor, limit-1, round+1, alpha, beta)
            if bv < cbv:
                cbv = bv
                bestMove = successor.move
                beta = bv
            if beta <= alpha:
                break
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove