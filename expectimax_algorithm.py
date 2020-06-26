import evaluation_functions
import pygame2048


class AI:
    def __init__(self):
        self.monotonicity_weight = 50
        self.empty_weight = 300
        self.merges_weight = 1000
        self.total_weight = 10

    def evaluate_board(self, grid_):
        utility = 0
        monotonicity = evaluation_functions.monotonicity(grid_)
        empty_merges_total = evaluation_functions.total_empty_and_merges(grid_)
        utility += monotonicity * self.monotonicity_weight
        utility += empty_merges_total[0] * self.empty_weight
        utility += empty_merges_total[1] * self.merges_weight
        utility += empty_merges_total[2] * self.total_weight
        return utility

    def maximise(self, grid_, depth=0):
        utilities = []
        grids = [pygame2048.left(grid_), pygame2048.right(grid_), pygame2048.up(grid_), pygame2048.down(grid_)]
        for _ in grids:
            utilities.append(self.chance(_, depth + 1))
        if depth == 0:
            return utilities
        else:
            return max(utilities)

    def chance(self, grid_, depth):
        average_utility = 0
        probabilities = evaluation_functions.probabilities(grid_)
        if probabilities:
            if depth >= 4:
                for _ in probabilities:
                    average_utility += self.evaluate_board(_[0]) * _[1]
                return average_utility
            for _ in probabilities:
                average_utility += _[1] * self.maximise(_[0], depth + 1)
            return average_utility
        else:
            return self.evaluate_board(grid_)

    def get_best_move(self, grid_):
        moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']
        array_ = self.maximise(grid_)
        index = array_.index(max(array_))
        return moves[index]
