def minmaxNaive(state, limit):
    """
    Naive Minmax algorithm
    :param state: current state of game, class GameState
    :param limit: an integer that indicates limit
    :return: cbv, best move
    """
    currentState = state.deepCopy()
    if limit == 0:
        return currentState.bestValue, currentState.move
    listOfSuccessor = currentState.getSuccessors()
    if currentState.minMax == 'max':
        cbv = float("-inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move = minmaxNaive(successor, limit-1)
            if bv > cbv:
                cbv = bv
                bestMove = successor.move
        return cbv, bestMove
    else:
        cbv = float("inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move = minmaxNaive(successor, limit-1)
            if bv < cbv:
                cbv = bv
                bestMove = successor.move
        return cbv, bestMove


def minmaxAlphaBeta(state, limit, alpha, beta):
    """
    Minmax algorithm with Alpha-Beta pruning.
    :param state:
    :param limit:
    :return:
    """
    currentState = state.deepCopy()
    if currentState.level == limit:
        return currentState.bestValue, currentState.move
    listOfSuccessor = currentState.getSuccessors()
    if currentState.minMax == "max":
        cbv = float("-inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move = minmaxAlphaBeta(successor, limit+1)
            if bv > cbv:
                cbv = bv
                bestMove = successor.move
            alpha = max(alpha, cbv)
            if beta <= alpha:
                break
        return cbv, bestMove
    else:
        cbv = float("inf")
        bestMove = None
        for successor in listOfSuccessor:
            bv, move = minmaxAlphaBeta(successor, limit+1)
            if bv < cbv:
                cbv = bv
                bestMove = successor.move
            beta = min(beta, cbv)
            if beta <= alpha:
                break
        return cbv, bestMove