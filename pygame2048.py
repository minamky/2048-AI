import random
import pygame
from pygame.time import Clock
from math import log

if __name__ == '__main__':
    pygame.init()
    clock = Clock()
    win = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("2048")

bg = pygame.image.load(r'images\background.png')
tiles = [pygame.image.load(r'images\2.png'), pygame.image.load(r'images\4.png'), pygame.image.load(r'images\8.png'),
         pygame.image.load(r'images\16.png'), pygame.image.load(r'images\32.png'),
         pygame.image.load(r'images\64.png'), pygame.image.load(r'images\128.png'),
         pygame.image.load(r'images\256.png'), pygame.image.load(r'images\512.png'),
         pygame.image.load(r'images\1024.png'), pygame.image.load(r'images\2048.png'),
         pygame.image.load(r'images\4096.png')]

# initialise the grid
grid = [[0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [0, 0, 0, 0]]

score = 0

coordinates = [[(14, 14), (136, 14), (258, 14), (380, 14)],
               [(14, 136), (136, 136), (258, 136), (380, 136)],
               [(14, 258), (136, 258), (258, 258), (380, 258)],
               [(14, 380), (136, 380), (258, 380), (380, 380)]]

tiles_ = []


class Tile:
    def __init__(self, x, y, value):
        self.x = x
        self.y = y
        self.value = value
        self.rect = pygame.Rect(self.x, self.y, 107, 107)

    def draw(self):
        win.blit(tiles[self.value], (self.x, self.y))


# initial spawn of 2 random tiles
def init_spawn_tiles(grid_):
    for i in range(2):
        x = random.randint(0, 3)
        y = random.randint(0, 3)
        value = random.random()
        if value < 0.9:
            value = 2
        else:
            value = 4
        while is_occupied(y, x, grid_):
            x = random.randint(0, 3)
            y = random.randint(0, 3)
        grid_[y][x] = value


# check if a particular position is occupied
def is_occupied(y, x, grid_):
    if grid_[y][x] == 0:
        return False
    return True


# check if all spaces are occupied
def is_all_occupied(grid_):
    list_ = []
    for y in range(len(grid_)):
        for x in range(len(grid_)):
            list_.append(is_occupied(y, x, grid_))
    if False in list_:
        return False
    else:
        return True


def spawn_tile(grid_):
    if grid_ == up(grid_) and grid_ == down(grid_) and grid_ == left(grid_) and grid_ == right(grid_):
        return
    x = random.randint(0, 3)
    y = random.randint(0, 3)
    value = random.random()
    if value < 0.9:
        value = 2
    else:
        value = 4
    if is_all_occupied(grid_):
        return
    while is_occupied(y, x, grid_):
        x = random.randint(0, 3)
        y = random.randint(0, 3)
    grid_[y][x] = value


# move the values left and adds them up into one value if they are the same
def move_left(column, scoring=False):
    global score
    returned_column = [0, 0, 0, 0]
    j = 0
    previous_value = None
    for i in range(4):
        # skip if the number is zero
        if column[i] != 0:
            # if its the first value in the list, set it to previous
            if previous_value is None:
                previous_value = column[i]
            else:
                # if the next value is equals to the previous, add them together and add it to the new column
                # increment the index of the new column
                if previous_value == column[i]:
                    returned_column[j] = 2 * column[i]
                    if scoring:
                        score += returned_column[j]
                    j += 1
                    previous_value = None
                # if not, set the current index of the new column to the previous value and increment the index of
                # the new column, and set the previous value to the current iteration of the column
                else:
                    returned_column[j] = previous_value
                    j += 1
                    previous_value = column[i]
    # add the last previous value (if any) into the new_column
    if previous_value is not None:
        returned_column[j] = previous_value
    return returned_column


def transpose_array(grid_):
    for i in range(len(grid_) - 1):
        for j in range(len(grid_)):
            if j >= i:
                temp = grid_[i][j]
                grid_[i][j] = grid_[j][i]
                grid_[j][i] = temp
    return grid_


def switch_sides(grid_):
    i = 1
    for _ in range(len(grid_) // 2):
        for j in range(len(grid_)):
            temp = grid_[j][_]
            grid_[j][_] = grid_[j][len(grid_) - i]
            grid_[j][len(grid_) - i] = temp
        i += 1


def rotate_90(grid_):
    switch_sides(transpose_array(grid_))
    return grid_


def rotate_180(grid_):
    return rotate_90(rotate_90(grid_))


def rotate_270(grid_):
    return rotate_90(rotate_90(rotate_90(grid_)))


def left(grid_, scoring=False):
    new_grid = []
    for _ in grid_:
        new_column = move_left(_, scoring)
        new_grid.append(new_column)
    return new_grid


def down(grid_, scoring=False):
    new_grid = []
    grid_ = rotate_90(grid_)
    for _ in grid_:
        new_grid.append(move_left(_, scoring))
    new_grid = rotate_270(new_grid)
    grid_ = rotate_270(grid_)
    return new_grid


def right(grid_, scoring=False):
    new_grid = []
    grid_ = rotate_180(grid_)
    for _ in grid_:
        new_grid.append(move_left(_, scoring))
    new_grid = rotate_180(new_grid)
    grid_ = rotate_180(grid_)
    return new_grid


def up(grid_, scoring=False):
    new_grid = []
    grid_ = rotate_270(grid_)
    for _ in grid_:
        new_grid.append(move_left(_, scoring))
    new_grid = rotate_90(new_grid)
    grid_ = rotate_90(grid_)
    return new_grid


def check_game_over(grid_):
    if is_all_occupied(grid_):
        if grid_ == up(grid_) and grid_ == down(grid_) and grid_ == left(grid_) and grid_ == right(grid_):
            return True
        else:
            return False
    else:
        return False


def check_max(grid_):
    highest = 0
    for y in range(len(grid)):
        for x in range(len(grid)):
            if grid_[y][x] > highest:
                highest = grid_[y][x]
    return highest


# main loop for terminal
def main_terminal():
    global grid
    init_spawn_tiles(grid)
    print(grid[0], "\n")
    print(grid[1], "\n")
    print(grid[2], "\n")
    print(grid[3], "\n")
    while True:
        if check_game_over(grid):
            print("game_over")
            return print(score)
        user_input = input("enter the direction to move in:")
        if user_input == '1':
            grid = up(grid)
            spawn_tile(grid)
            print(grid[0], "\n")
            print(grid[1], "\n")
            print(grid[2], "\n")
            print(grid[3], "\n")
        elif user_input == '2':
            grid = down(grid)
            spawn_tile(grid)
            print(grid[0], "\n")
            print(grid[1], "\n")
            print(grid[2], "\n")
            print(grid[3], "\n")
        elif user_input == '3':
            grid = left(grid)
            spawn_tile(grid)
            print(grid[0], "\n")
            print(grid[1], "\n")
            print(grid[2], "\n")
            print(grid[3], "\n")
        elif user_input == '4':
            grid = right(grid)
            spawn_tile(grid)
            print(grid[0], "\n")
            print(grid[1], "\n")
            print(grid[2], "\n")
            print(grid[3], "\n")
        else:
            print("INVALID INPUT!")


def redraw_screen():
    global tiles_
    win.blit(bg, (0, 0))
    for _ in tiles_:
        _.draw()
    pygame.display.update()


# based on the grid generate tile objects
def generate_tiles():
    global grid
    global tiles_
    tiles_ = []
    for y in range(len(grid)):
        for x in range(len(grid)):
            if grid[y][x] != 0:
                tiles_.append(Tile(coordinates[y][x][0], coordinates[y][x][1], int(log((grid[y][x]), 2) - 1)))


def main():
    run = True
    global grid
    global tiles_
    global score
    clock.tick(15)
    init_spawn_tiles(grid)
    generate_tiles()
    redraw_screen()
    while run:
        clock.tick(30)
        if check_game_over(grid):
            print("GAME OVER")
            return print(score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    grid = up(grid, True)
                    spawn_tile(grid)
                    generate_tiles()
                    redraw_screen()
                    print(score)
                elif event.key == pygame.K_DOWN:
                    grid = down(grid, True)
                    spawn_tile(grid)
                    generate_tiles()
                    redraw_screen()
                    print(score)
                elif event.key == pygame.K_LEFT:
                    grid = left(grid, True)
                    spawn_tile(grid)
                    generate_tiles()
                    redraw_screen()
                    print(score)
                elif event.key == pygame.K_RIGHT:
                    grid = right(grid, True)
                    spawn_tile(grid)
                    generate_tiles()
                    redraw_screen()
                    print(score)


import evaluation_functions


class AI:
    def __init__(self):
        self.monotonicity_weight = 50
        self.empty_weight = 400
        self.merges_weight = 500
        self.total_weight = 100

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
        grids = [left(grid_), right(grid_), up(grid_), down(grid_)]
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
            if depth >= 3:
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
        if evaluation_functions.total_empty_and_merges(grid_)[0] == 0:
            if grid_ == left(grid_):
                array_[0] = 0
            if grid_ == right(grid_):
                array_[1] = 0
            if grid_ == up(grid_):
                array_[2] = 0
            if grid_ == down(grid_):
                array_[3] = 0
        index = array_.index(max(array_))
        return moves[index]


ai = AI()


def main_ai():
    run = True
    global grid
    global tiles_
    global score
    clock.tick(15)
    init_spawn_tiles(grid)
    generate_tiles()
    redraw_screen()
    while run:
        if check_game_over(grid):
            print("GAME OVER")
            return print(score, check_max(grid))
        move = ai.get_best_move(grid)
        print(move)
        if move == 'UP':
            grid = up(grid, True)
            spawn_tile(grid)
            generate_tiles()
            redraw_screen()
            print(score)
        elif move == 'DOWN':
            grid = down(grid, True)
            spawn_tile(grid)
            generate_tiles()
            redraw_screen()
            print(score)
        elif move == 'LEFT':
            grid = left(grid, True)
            spawn_tile(grid)
            generate_tiles()
            redraw_screen()
            print(score)
        elif move == 'RIGHT':
            grid = right(grid, True)
            spawn_tile(grid)
            generate_tiles()
            redraw_screen()
            print(score)


# if __name__ == '__main__':
#     main()
#     pygame.quit()

main_ai()
pygame.quit()
