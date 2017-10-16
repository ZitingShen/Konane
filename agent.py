from game import GameState


def minmaxNaive(state, limit):
    """
    Naive Minmax algorithm
    :param state: current state of game, class GameState
    :param limit: an integer that indicates limit
    :return: cbv, best move
    """
    cur_state = state.deepCopy()
    if cur_state.level == limit:
        return cur_state.bestValue, cur_state.move
    listOfSuccessor = cur_state.getSuccessors()
    if cur_state.minMax == "max":
        cbv = float("-inf")
        bestMove = None
        for n in listOfSuccessor:
            bv, move = minmaxNaive(n, limit+1)
            if bv > cbv:
                cbv = bv
                bestMove = move
        return cbv, bestMove
    else:
        cbv = float("inf")
        bestMove = None
        for n in listOfSuccessor:
            bv, move = minmaxNaive(n, limit+1)
            if bv < cbv:
                cbv = bv
                bestMove = move
        return cbv, bestMove


def minmaxAlphaBetaPruning(state):
    """
    Minmax algorithm with Alpha-Beta pruning.
    """
