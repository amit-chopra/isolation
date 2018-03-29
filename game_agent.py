

import random


class SearchTimeout(Exception):
    pass


def custom_score(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    if my_moves == 0:
        return float("-inf")

    if opponent_moves == 0:
        return float("inf")

    return my_moves/opponent_moves


def custom_score_2(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return my_moves - 1.5 * opponent_moves


def custom_score_3(game, player):

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    my_moves = len(game.get_legal_moves(player))
    opponent_moves = len(game.get_legal_moves(game.get_opponent(player)))

    return 1.5 * my_moves - opponent_moves


class IsolationPlayer:

    def __init__(self, search_depth=3, score_fn=custom_score, timeout=50.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):

    def get_move(self, game, time_left):
        self.time_left = time_left
        best_move = (-1, -1)

        try:
            return self.minimax(game, self.search_depth)

        except SearchTimeout:
            pass
        return best_move

    def __min_value(self, game, depth):
        self.__check_time()
        if self.__is_terminal(game, depth):
            return self.score(game, self)
        min_val = float("inf")
        legal_moves = game.get_legal_moves()
        for move in legal_moves:
            forecast = game.forecast_move(move)
            min_val = min(min_val, self.__max_value(forecast, depth - 1))
        return min_val

    def __max_value(self, game, depth):
        self.__check_time()
        if self.__is_terminal(game, depth):
            return self.score(game, self)
        max_val = float("-inf")
        legal_moves = game.get_legal_moves()
        for move in legal_moves:
            forecast = game.forecast_move(move)
            max_val = max(max_val, self.__min_value(forecast, depth - 1))
        return max_val

    def __is_terminal(self, game, depth):

        self.__check_time()
        if len(game.get_legal_moves()) != 0 and depth > 0:
            return False
        return True

    def __check_time(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

    def minimax(self, game, depth):
        self.__check_time()
        legal_moves = game.get_legal_moves()
        if not legal_moves:
            return (-1, -1)
        valuez = [(self.__min_value(game.forecast_move(m), depth - 1), m) for m in legal_moves]
        move = max(valuez)
        return move



class AlphaBetaPlayer(IsolationPlayer):

    def get_move(self, game, time_left):

        # TODO: finish this function!
        legal_moves = game.get_legal_moves(self)
        if len(legal_moves) > 0:
            best_move = legal_moves[randint(0, len(legal_moves)-1)]
        else:
            best_move = (-1, -1)
        try:
            depth = 1
        while True:
             current_move = self.alphabeta(game, depth, alpha, beta)
                if current_move == (-1, -1):
                    return best_move
                else:
                    best_move = current_move
                depth += 1
        except SearchTimeout:
            return best_move
        return best_move



    def __max_value(player, game, depth, alpha, beta):
        self.__check_time()
        best_move = (-1, -1)
        if self.__is_terminal(game, depth):
            return (self.score(game, self), best_move)
        value = float("-inf")
        legal_moves = game.get_legal_moves()
        for move in legal_moves:
            result = self.__min_value(game.forecast_move(move), depth - 1, alpha, beta)
            if result[0] > value:
                value = result
                best_move = move
            if value >= beta:
                return (value, best_move)
            alpha = max(alpha, value)
        return (value, best_move)


    def __min_value(player, game, depth, alpha, beta):
        self.__check_time()
        best_move = (-1, -1)
        if self.__is_terminal(game, depth):
            return (self.score(game, self), best_move)
        value = float("inf")
        legal_moves = game.get_legal_moves()
        for move in legal_moves:
            result = self.__max_value(game.forecast_move(move), depth - 1, alpha, beta)
            if result[0] < value:
                value = result
                best_move = move
            if value <= alpha:
                return (value, best_move)
            beta = min(beta, value)
        return (value, best_move)

    def __is_terminal(self, game, depth):
        self.__check_time()
        if len(game.get_legal_moves()) != 0 and depth > 0:
            return False
        return True

    def __check_time(self):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

     def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        self.__check_time()
        move = self.__max_value(game, depth, alpha, beta)
        return move
