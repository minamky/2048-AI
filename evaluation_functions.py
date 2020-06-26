import copy


def monotonicity(grid_):
    # totals[0] increase left to right
    # totals[1] decrease left to right
    # totals[2] increase up to down
    # totals[3] decrease up to down
    totals = [0, 0, 0, 0]
    # calculate monotonicity for left to right
    for y in range(4):
        x = 0
        while x < 4:
            if grid_[y][x] == 0:
                x += 1
                continue
            else:
                next_ = search_non_zero(grid_[y], x)
                if next_:
                    if grid_[y][next_] - grid_[y][x] > 0:
                        totals[0] += grid_[y][x] - grid_[y][next_]
                        x += 1
                    else:
                        totals[1] += grid_[y][next_] - grid_[y][x]
                        x += 1
                else:
                    break

    _grid = []
    for x in range(4):
        row = []
        for y in range(4):
            row.append(grid_[y][x])
        _grid.append(row)
    # calculate monotonicity for up to down
    for x in range(4):
        y = 0
        while y < 4:
            if grid_[y][x] == 0:
                y += 1
                continue
            else:
                next_ = search_non_zero(_grid[x], y)
                if next_:
                    if grid_[next_][x] - grid_[y][x] > 0:
                        totals[2] += grid_[y][x] - grid_[next_][x]
                        y += 1
                    else:
                        totals[3] += grid_[next_][x] - grid_[y][x]
                        y += 1
                else:
                    break
    return max(totals[0], totals[1]) + max(totals[2], totals[3])


def search_non_zero(row, index):
    for _ in range(index+1, 4):
        if row[_] != 0:
            next_ = _
            return next_
    else:
        return None


def merges_and_empty(grid_, axis=1):
    empty = 0
    merges = 0
    for y in range(4):
        x = 0
        while x < 4:
            if grid_[y][x] == 0:
                x += 1
                empty += 1
                continue
            else:
                next_ = search_non_zero(grid_[y], x)
                if next_:
                    if grid_[y][x] == grid_[y][next_]:
                        empty += (next_ - x - 1)
                        merges += 1
                        x = next_
                        x += 1
                    else:
                        x += 1
                else:
                    empty += (3 - x)
                    break
    if axis == 1:
        return [empty, merges]
    else:
        return [0, merges]


# counts number of empty squares and potential merges
def total_empty_and_merges(grid_):
    total = 0
    _grid = []
    # transpose the grid
    for x in range(4):
        row = []
        for y in range(4):
            total += grid_[y][x]
            row.append(grid_[y][x])
        _grid.append(row)
    return [merges_and_empty(grid_)[0] + merges_and_empty(_grid, axis=0)[0],
            merges_and_empty(grid_)[1] + merges_and_empty(_grid, axis=0)[1],
            total]


# returns the probability of a particular grid happening AFTER a movement
def probabilities(grid_):
    empty_spaces = total_empty_and_merges(grid_)[0]
    if empty_spaces == 0:
        return None
    empty_spaces = 1/empty_spaces
    probability_array = []
    for y in range(4):
        for x in range(4):
            if grid_[y][x] == 0:
                grid_1 = copy.deepcopy(grid_)
                grid_2 = copy.deepcopy(grid_)
                grid_1[y][x] = 2
                grid_2[y][x] = 4
                probability_array.append([grid_1, 0.9*empty_spaces])
                probability_array.append([grid_2, 0.1*empty_spaces])
    return probability_array
