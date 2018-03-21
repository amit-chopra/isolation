
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
        """Helper method to check if we've reached the end of the game tree or
        if the maximum depth has been reached.
        """
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
        vals = [(self.__min_value(game.forecast_move(m), depth - 1), m) for m in legal_moves]
        _, move = max(vals)
        return move

class AlphaBetaPlayer(IsolationPlayer):

    def get_move(self, game, time_left):

        self.time_left = time_left

        # TODO: finish this function!
        result = (-1, -1)

        if len(game.get_legal_moves()) == 0:
            return result

        for depth in range(1, len(game.get_blank_spaces())):
            try:
                result = self.alphabeta(game, depth)
            except SearchTimeout:
                return result


    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):

        def time_test(player):
            if player.time_left() < player.TIMER_THRESHOLD:
                raise SearchTimeout()

        legal_moves = game.get_legal_moves()

        if len(legal_moves) == 0:
            return (-1,-1)


        def terminal_test(game):

            return not bool(game.get_legal_moves())  

        def max_value(player, game, depth, alpha, beta):
            time_test(player)

            if terminal_test(game):
                return float("-inf")

            if depth <= 0:
                return player.score(game, player)
            v = float("-inf")
            for m in game.get_legal_moves():
                v = max(v, min_value(player, game.forecast_move(m), depth - 1, alpha, beta))

                if v >= beta:
                    return v

                alpha = max(alpha, v)

            return v


        def min_value(player, game, depth, alpha, beta):
            time_test(player)

            if terminal_test(game):
                return float("inf")

            if depth <= 0:
                return player.score(game, player)
            v = float("inf")
            for m in game.get_legal_moves():
                v = min(v, max_value(player, game.forecast_move(m), depth - 1, alpha, beta))

                if v <= alpha:
                    return v

                beta = min(beta, v)

            return v


        def mmd(player, game, depth, alpha, beta):
            v = float("-inf")
            move = (-1, -1)
            for m in game.get_legal_moves():
                mmv = min_value(player, game.forecast_move(m), depth - 1, alpha, beta)
                if mmv > v:
                    v = mmv
                    move = m

                alpha = max(alpha, v)

            return move

        return mmd(self, game, depth, alpha, beta)
