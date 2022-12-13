"""
Advent of code - day 12
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path
import numpy as np


def get_valid_grid_locations(grid, visited_grid, i, j):
    """
    Returns valid grid location from a certain position-
    :param grid: (np.array) the elevation grid
    :param visited_grid: (np.array) boolean grid representing visited tiles
    :param i: (int) ith location
    :param j: (int) jth location
    :return: (list) list of tuples with valid 2d locations
    """
    locations = []
    if i > 0:
        if grid[i-1, j] - grid[i, j] <= 1 and not visited_grid[i-1, j]:
            locations.append((i-1, j))
            visited_grid[i-1, j] = True
    if i < grid.shape[0] - 1:
        if grid[i+1, j] - grid[i, j] <= 1 and not visited_grid[i+1, j]:
            locations.append((i+1, j))
            visited_grid[i+1, j] = True
    if j > 0:
        if grid[i, j - 1] - grid[i, j] <= 1 and not visited_grid[i, j-1]:
            locations.append((i, j - 1))
            visited_grid[i, j-1] = True

    if j < grid.shape[1] - 1:
        if grid[i, j + 1] - grid[i, j] <= 1 and not visited_grid[i, j + 1]:
            locations.append((i, j + 1))
            visited_grid[i, j+1] = True

    if not locations:
        return []
    return locations


class Level:
    """
    Class representing a level (of a breadth-first depth search).
    """
    def __init__(self, parent=None, child=None, indices=[], index=0):
        """
        Initializes a level.
        :param parent: (Level) optional parent level
        :param child: (Level) optional child level
        :param indices: (list) list of tuples representing elevation locations belonging to this
                        level
        :param index: (int) depth level
        """
        self.parent = parent
        self.child = child

        self.indices = indices
        self.index = index

    def propagate(self, grid, visited_grid):
        """
        Calculates the (depth-wise) next level.
        :param grid: (np.array) the elevation grid
        :param visited_grid: (np.array) boolean grid representing visited tiles
        :return: (int) the level's depth if it has found the top
        """
        child_indices, child_elevations = [],  []
        for (i, j) in self.indices:
            valid_locations = get_valid_grid_locations(grid, visited_grid, i=i, j=j)

            for valid_location in valid_locations:
                child_indices.append(valid_location)
                child_elevations.append(grid[valid_location[0], valid_location[1]])

        if not child_indices:
            return -1

        child_level = Level(parent=self, child=None, indices=child_indices, index=self.index + 1)
        self.child = child_level

        if 27 in child_elevations:
            return self.child.index
        return self.child.propagate(grid=grid, visited_grid=visited_grid)


def get_valid_starting_positions(grid, part_2=False):
    """
    Returns a list of valid starting positions.
    :param grid: (np.array) 2d array representing the elevations
    :param part_2: (bool) whether to compute results for part 1 or part 2
    :return:
    """
    if part_2:
        grid[grid != 0] -= 1

    starting_positions = np.stack(np.where(grid == 0)).T.tolist()
    if part_2:
        grid += 1
    return starting_positions


def day12():
    """
    Prints the results for the two day 12 riddles.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 12. Run "
                                                 "`python day12/day12.py` for the first part, "
                                                 "and `python day12/day12.py --part-2` for the "
                                                 "second part.")
    parser.add_argument('--part-2', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        grid = np.array([[ord(l) for l in line.strip()] for line in file.readlines()])

    # do a few modifications such that computation is easier
    grid -= 96
    grid[grid == -13] = 0
    grid[grid == -27] = 27

    valid_starting_positions = get_valid_starting_positions(grid, part_2=args.part_2)

    path_lenghts = []
    for starting_position in valid_starting_positions:
        start_i, start_j = starting_position

        visited_grid = np.zeros_like(grid).astype(bool)
        visited_grid[start_i, start_j] = True

        first_level = Level(parent=None, child=None, indices=[(int(start_i), int(start_j))],
                            index=0)
        last_index = first_level.propagate(grid=grid, visited_grid=visited_grid)
        if last_index != -1:
            path_lenghts.append(last_index)

    print(f"Number of steps for the shortest path: {min(path_lenghts)}")


if __name__ == '__main__':
    day12()
