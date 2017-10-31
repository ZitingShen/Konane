import random

def minimaxNaive(state, limit, round):
    """
    Naive Minmax algorithm
    :param state: current state of game, class GameState
    :param limit: an integer that indicates limit
    :return: cbv, best move, number of evaluations
    """
    numberEvaluate = 0

    if limit == 0:
        state.bestValue = state.evaluate()
        numberEvaluate += 1
        return state.bestValue, state.move, numberEvaluate

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
            bv, move, successorEvaluate = minimaxNaive(successor, limit-1, round+1)
            numberEvaluate += successorEvaluate
            if bv > cbv:
                cbv = bv
                bestMove = successor.move
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove, numberEvaluate
    else:
        cbv = float("inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move, successorEvaluate = minimaxNaive(successor, limit-1, round+1)
            numberEvaluate += successorEvaluate
            if bv < cbv:
                cbv = bv
                bestMove = successor.move
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove, numberEvaluate


def minimaxAlphaBeta(state, limit, round, alpha, beta):
    """
    Minmax algorithm with Alpha-Beta pruning.
    :param state: current state of game, class GameState
    :param limit: an integer that indicates limit
    :param alpha: the min value of the max level
    :param beta: the max value of the min level
    :return: cbv, best move, number of evaluations
    """
    numberEvaluate = 0

    if limit == 0:
        state.bestValue = state.evaluate()
        numberEvaluate += 1
        return state.bestValue, state.move, numberEvaluate

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
            bv, move, successorEvaluate = minimaxAlphaBeta(successor, limit-1, round+1, alpha, beta)
            numberEvaluate += successorEvaluate
            if bv > cbv:
                cbv = bv
                bestMove = successor.move
                alpha = bv
            if beta <= alpha:
                break
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove, numberEvaluate
    else:
        cbv = float("inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move, successorEvaluate = minimaxAlphaBeta(successor, limit-1, round+1, alpha, beta)
            numberEvaluate += successorEvaluate
            if bv < cbv:
                cbv = bv
                bestMove = successor.move
                beta = bv
            if beta <= alpha:
                break
        if listOfSuccessor and bestMove == None:
            bestMove = random.choice(listOfSuccessor).move
        return cbv, bestMove, numberEvaluate