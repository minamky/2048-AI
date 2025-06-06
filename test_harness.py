import pygame2048
import evaluation_functions
import copy
import time

import pygame
pygame.display.set_mode = lambda x: None
pygame.display.update = lambda: None
pygame.image.load = lambda x: None
import random

class testGame:
    def __init__(self, use_snake=False, use_corner=False, use_smoothness=False, penalize_large_scattered=False, use_clustering=False, use_min_adjacent_diff=False):
        #weights for heuristics provided in repo
        self.monotonicity_weight = 50
        self.empty_weight = 400
        self.merges_weight = 500
        self.total_weight = 100

        if use_snake:
            self.use_snake = True
            self.snake_weight = 100
        else:
            self.snake_weight = 0
            self.use_snake = False

        if use_corner:
            self.use_corner = True
            self.corner_weight = 100
        else:
            self.use_corner = False
            self.corner_weight = 0

        # if use_smoothness:
        #     self.use_smoothness = True
        #     self.smoothness_weight = 10
        # else:
        #     self.use_smoothness = False
        #     self.smoothness_weight = 0

        if use_clustering:
            self.use_clustering = True
            self.clustering_weight = -10
        else: 
            self.use_clustering = False
            self.clustering_weight = 0
        if penalize_large_scattered:
            self.penalize_large_scattered = True
            self.penalize_large_scattered_weight = -10
        else:
            self.penalize_large_scattered = False
            self.penalize_large_scattered_weight = 0
        if use_min_adjacent_diff:
            self.min_adjacent_diff = True
            self.min_adjacent_diff_weight = 10
        else:
            self.min_adjacent_diff = False
            self.min_adjacent_diff_weight = 0


    #extension of the evaluate board function provided in the bsae repository 
    def evaluate_board(self, grid_):
        #code from repo
        utility = 0
        monotonicity = evaluation_functions.monotonicity(grid_)
        empty_merges_total = evaluation_functions.total_empty_and_merges(grid_)
        utility += monotonicity * self.monotonicity_weight
        utility += empty_merges_total[0] * self.empty_weight
        utility += empty_merges_total[1] * self.merges_weight
        utility += empty_merges_total[2] * self.total_weight

        
        corner_score = evaluation_functions.corner_heuristic(grid_) * self.corner_weight
        chain = evaluation_functions.chaining(grid_) * self.snake_weight
        # smoothness_score = evaluation_functions.smoothness_heuristic(grid_) * self.smoothness_weight

        clustering_score = evaluation_functions.clustering(grid_) * self.clustering_weight
        largeScattered_score = evaluation_functions.penalize_large_scattered(grid_) * self.penalize_large_scattered_weight
        min_adjacent_diff = evaluation_functions.min_adjacent_diff(grid_) * self.min_adjacent_diff_weight

        utility += corner_score + chain + clustering_score + largeScattered_score + min_adjacent_diff  
        return utility

    #code copied from repo
    def maximise(self, grid_, depth=0):
        utilities = []
        grids = [pygame2048.left(grid_), pygame2048.right(grid_), 
                pygame2048.up(grid_), pygame2048.down(grid_)]
        for _ in grids:
            utilities.append(self.chance(_, depth + 1))
        if depth == 0:
            return utilities
        else:
            return max(utilities)

    #code copied from repo
    def chance(self, grid_, depth):
        average_utility = 0
        probabilities = evaluation_functions.probabilities(grid_)
        if probabilities:
            #we enforce depth limit 3 like the repo does. For future work, would be cool to make this adaptable
            if depth >= 3:  
                for _ in probabilities:
                    average_utility += self.evaluate_board(_[0]) * _[1]
                return average_utility
            for _ in probabilities:
                average_utility += _[1] * self.maximise(_[0], depth + 1)
            return average_utility
        else:
            return self.evaluate_board(grid_)

    #code copied from repo
    def get_best_move(self, grid_):
        moves = ['LEFT', 'RIGHT', 'UP', 'DOWN']
        array_ = self.maximise(grid_)
        if evaluation_functions.total_empty_and_merges(grid_)[0] == 0:
            if grid_ == pygame2048.left(grid_):
                array_[0] = 0
            if grid_ == pygame2048.right(grid_):
                array_[1] = 0
            if grid_ == pygame2048.up(grid_):
                array_[2] = 0
            if grid_ == pygame2048.down(grid_):
                array_[3] = 0
        index = array_.index(max(array_))
        return moves[index]
    
 
def find_max_tile(grid_):
    maxTile= 0
    for row in range(len(grid_)):
        for col in range(len(grid_[0])):
            if grid_[row][col] > maxTile:
                maxTile = grid_[row][col]
    return maxTile

#our adapted version of code from repo
def run_single_game(ai, max_moves=2000, verbose=False):
    pygame2048.score = 0
    #start with blAnk grid for 2048
    grid = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    
    pygame2048.init_spawn_tiles(grid)
    
    moves_made = 0
    reaching2048 = False
    
    while not pygame2048.check_game_over(grid) and moves_made < max_moves:
        move = ai.get_best_move(grid)

        moves_made += 1
        maxVal = find_max_tile(grid)
        if maxVal >= 2048:
            reaching2048 = True
        
        if move == 'UP':
            grid = pygame2048.up(grid, True)
            pygame2048.spawn_tile(grid)
        elif move == 'DOWN':
            grid = pygame2048.down(grid, True)
            pygame2048.spawn_tile(grid)
        elif move == 'LEFT':
            grid = pygame2048.left(grid, True)
            pygame2048.spawn_tile(grid)
        elif move == 'RIGHT':
            grid = pygame2048.right(grid, True)
            pygame2048.spawn_tile(grid)

    final_score = pygame2048.score
    max_tile = max(max(row) for row in grid if any(row))
   
    print(f"Game finish: Score={final_score}")
    print(f"Max ={max_tile}")
    print(f"num Moves={moves_made}")
    print("\n\n")
    
    return final_score, max_tile, moves_made, reaching2048

#adapted from repo for testing games
def game_random(ai, max_moves=1000, verbose=False):
    pygame2048.score = 0
    grid = [[0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    
    pygame2048.init_spawn_tiles(grid)
    
    moves_made = 0
    reached2048 = False
    
    while not pygame2048.check_game_over(grid) and moves_made < max_moves:
        move = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

        moves_made += 1
        maxVal = find_max_tile(grid)
        if maxVal >= 2048:
            reached2048 = True
        print("BEREAKING OUT OF LOOP")
        
        if move == 'UP':
            grid = pygame2048.up(grid, True)
            pygame2048.spawn_tile(grid)
        elif move == 'DOWN':
            grid = pygame2048.down(grid, True)
            pygame2048.spawn_tile(grid)
        elif move == 'LEFT':
            grid = pygame2048.left(grid, True)
            pygame2048.spawn_tile(grid)
        elif move == 'RIGHT':
            grid = pygame2048.right(grid, True)
            pygame2048.spawn_tile(grid)

    final_score = pygame2048.score
    max_tile = max(max(row) for row in grid if any(row))
    print(f"Game finish: Score={final_score}")
    print(f"Max ={max_tile}")
    print(f"num Moves={moves_made}")
    print("\n\n")
    
    return final_score, max_tile, moves_made, reached2048



def verify_single_config(flags):
    ai = testGame(flags)
    score, max_tile, moves, reached2048 = run_single_game(ai, verbose=True)
    print(f"Game finish: Score={score}")
    print(f"Max ={max_tile}")
    print(f"num Moves={moves}")
    print("\n\n")

    # print("getting here")
    
    return score, max_tile, moves, reached2048


if __name__ == "__main__":
    ai = testGame()
    game_random(ai)
    
    print(f"BaseLIne")
    verify_single_config({})
    
    print("snake")
    flags = {"use_snake": True}
    verify_single_config(flags)
    
    print("only corner")
    flags = {"use_corner": True}
    verify_single_config()
    
    # print("smoothness")
    # flags = {"use_smoothness": True}
    # verify_single_config(flags)
    print("snake + corner")
    flags = {"use_snake": True, "use_corner": True}
    verify_single_config(flags)
    

    print("smoothness + snake")
    flags = {"use_snake": True, "use_smoothness": True}
    verify_single_config(flags)

    print("smoothness + corner")
    flags = {"use_corner": True, "use_smoothness": True}
    verify_single_config(flags)
    
    print("snake + corner + smoothness")
    flags = {"use_snake": True, "use_corner": True, "use_smoothness": True}
    verify_single_config()
    print("clustering")
    flags={"use_clustering": True}
    verify_single_config(flags)
    print("scattered penalization")
    flags={"penalize_large_scattered": True}
    verify_single_config(flags)
    print("min adjacent only")
    flags={"use_min_adjacent_diff": True}
    verify_single_config(flags)
    
    print("all")
    flags={"use_snake": True, "use_corner": True, "use_smoothness": True, "use_clustering": True, "penalize_large_scattered": True, "use_min_adjacent_diff": True
    }
    verify_single_config(flags)
