"""
Advent of code - day 22, part 1
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path
import re
import numpy as np
import cv2


CW_TURNS = ['R', 'D', 'L', 'U']


def get_minmax_element_across_dim(coords, fixed_index=None, minmax=np.argmin, dim=0):
    """
    Helper function to return the min/max element of a set of i/j coordinates.
    :param coords: (set) set of 2d coordinates
    :param fixed_index: (int) fixed row/column index
    :param minmax: (function) one of np.argmin/np.argmax
    :param dim: (int) one of [0, 1] specifying ith or jth coordinate axis
    :return: (list) 2d coordinate
    """
    valid_coords = coords
    if fixed_index:
        valid_coords = [coord for coord in list(coords) if coord[1-dim] == fixed_index]
    return list(valid_coords)[minmax(np.array(list(valid_coords))[:, dim])]


class Grid:
    """
    Class representing a grid for simulating the puzzle input.
    """
    def __init__(self, open_tiles, walls, start_tile):
        """
        Initializes a grid.
        :param open_tiles: (set) set of 2d valid (step-able) coordinates
        :param walls: (set) set of 2d wall coordinates
        :param start_tile: (tuple) starting indices
        """
        self.open_tiles = open_tiles
        self.walls = walls
        self.current_i, self.current_j = start_tile
        self.current_direction = 'R'
        self.max_i, self.max_j = np.array(list(self.open_tiles.union(self.walls))).max(axis=0) + 1
        self.width = 5
        self.grid = self._initialize_grid()

    def move(self):
        """
        Moves once following the direction currently set. To speed things up, returns
        a boolean whether the move was successful or not.
        :return: (bool) boolean indicating whether the move was successful
        """
        if self.current_direction == 'R':
            next_tile = (self.current_i, self.current_j + 1)
        elif self.current_direction == 'L':
            next_tile = (self.current_i, self.current_j - 1)
        elif self.current_direction == 'U':
            next_tile = (self.current_i - 1, self.current_j)
        else:
            next_tile = (self.current_i + 1, self.current_j)

        # if next tile is not a wall: continue marching
        if not next_tile in self.walls:
            # check if the tile is a valid tile
            if next_tile in self.open_tiles:
                self.current_i, self.current_j = next_tile
            else:
                # wrap around
                if self.current_direction == 'R':  # get left-most tile
                    potential_i, potential_j = get_minmax_element_across_dim(
                        self.open_tiles.union(self.walls), fixed_index=next_tile[0],
                        minmax=np.argmin, dim=1)
                elif self.current_direction == 'L':  # get right-most tile
                    potential_i, potential_j = get_minmax_element_across_dim(
                        self.open_tiles.union(self.walls), fixed_index=next_tile[0],
                        minmax=np.argmax, dim=1)
                elif self.current_direction == 'U':  # get down-most tile
                    potential_i, potential_j = get_minmax_element_across_dim(
                        self.open_tiles.union(self.walls), fixed_index=next_tile[1],
                        minmax=np.argmax, dim=0)
                else:  # get up-most tile
                    potential_i, potential_j = get_minmax_element_across_dim(
                        self.open_tiles.union(self.walls), fixed_index=next_tile[1],
                        minmax=np.argmin, dim=0)
                # check if the potential next tile is a wall - if not, make a step
                # else: stay where we are
                if (potential_i, potential_j) not in self.walls:
                    self.current_i = potential_i
                    self.current_j = potential_j
            return True
        return False

    def turn(self, direction):
        """
        Turns (counter-)clock-wise.
        """
        current_index = CW_TURNS.index(self.current_direction)
        if direction == 'L':
            next_index = current_index - 1
        else:
            next_index = current_index + 1
            if next_index == 4:
                next_index = 0

        self.current_direction = CW_TURNS[next_index]

    def determine_password(self):
        """
        Determines the current password.
        """
        return 1000 * (self.current_i + 1) + 4 * (self.current_j + 1) + \
            CW_TURNS.index(self.current_direction)

    def _initialize_grid(self):
        """
        Initializes a grid for drawing.
        """
        grid = np.zeros((self.width * self.max_i, self.width * self.max_j), dtype=np.uint8)
        grid = self.update_grid(grid=grid, coords=self.open_tiles, symbol='dot')
        return self.update_grid(grid=grid, coords=self.walls, symbol='hashtag')

    def update_grid(self, grid, coords, symbol, fill=255, height_offset=0):
        """
        Updates the grid.
        :param grid: (np.array) 2d array representing the cave
        :param coords: (set) set of coordinates
        :param symbol: (str) symbol to use for plotting
        :param fill: (int) symbol fill value
        :return: (np.array) the updated grid
        """
        for (coord_i, coord_j) in coords:
            coord_i -= height_offset
            start_i, end_i, start_j, end_j = self._get_drawing_pos(coord_i=coord_i, coord_j=coord_j)
            grid[start_i:end_i, start_j:end_j] = self._get_symbol_for_drawing(symbol=symbol,
                                                                              fill=fill)
        return grid

    def _get_drawing_pos(self, coord_i, coord_j, size=5):
        """
        Helper to return the bounding box coordinates of the position to draw.
        :param coord_i: (int) i-th coordinate
        :param coord_j: (int) j-th coordinatet
        :return: (tuple) tuple of ints representing the bounding box
        """
        start_i = coord_i*size
        end_i = coord_i*size+size
        start_j = coord_j*size
        end_j = coord_j*size+size
        return start_i, end_i, start_j, end_j

    def _get_symbol_for_drawing(self, symbol='hashtag', fill=255):
        """
        Helper to return a symbol for the interactive visualization.
        :param symbol: (str) one of ['cube', 'plus', 'diamond']
        :param fill: (int) grayscale strength
        :return: (np.array) 2d array representing the symbol
        """
        area = np.zeros((self.width, self.width), dtype=np.uint8)
        if symbol == 'hashtag':
            area[1] = fill
            area[3] = fill
            area[:, 1] = fill
            area[:, 3] = fill
        elif symbol == 'dot':
            area[2, 2] = fill
        elif symbol in ['U', 'D']:
            for i in range(3):
                area[i + 1, i] = 255
                area[i + 1, 4 - i] = 255
            if symbol == 'U':
                area = np.flipud(area)
        elif symbol in ['L', 'R']:
            for i in range(3):
                area[i, i + 1] = 255
                area[4 - i, i + 1] = 255
            if symbol == 'L':
                area = np.fliplr(area)
        else:
            raise NotImplementedError
        return area

    def draw(self):
        """
        Adds the current position to the drawn grid and displays it.
        """
        # print current position
        grid = self.update_grid(grid=self.grid, coords={(self.current_i, self.current_j)},
                                symbol=self.current_direction)
        cv2.imshow('grid', grid)
        cv2.waitKey(50)


def day22_part1():
    """
    Prints the results for the day 22 part 1 riddle.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 22, part 1. Run "
                                                 "`python day22/day22_part1.py`. "
                                                 "Add `--viz` for a visualization.")
    parser.add_argument('--viz', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        data = [line.replace('\n', '') for line in file.readlines()]

    puzzle_map = data[:-2]
    movements = data[-1]

    # format puzzle map to open tiles and walls
    open_tiles = set()
    walls = set()

    start_tile = None
    for coord_i, puzzle_line in enumerate(puzzle_map):
        puzzle_line = np.array([ord(tile) for tile in puzzle_line])
        # valid tiles: 46
        # walls: 35
        open_tiles_j = np.where(puzzle_line == 46)[0]
        for coord_j in open_tiles_j:
            if not start_tile:
                start_tile = (coord_i, coord_j)
            open_tiles.add((coord_i, coord_j))
        walls_j = np.where(puzzle_line == 35)[0]
        for coord_j in walls_j:
            walls.add((coord_i, coord_j))

    grid = Grid(open_tiles=open_tiles, walls=walls, start_tile=start_tile)

    movements = list(filter(None, re.split(r'(\d+)', movements)))

    last_steps = None
    if len(movements) % 2 != 0:
        last_steps = movements.pop(-1)
    movements = [(int(movements[i]), movements[i+1]) for i in range(0, len(movements), 2)]

    for steps, direction in movements:
        for _ in range(steps):
            if args.viz:
                grid.draw()
            can_still_move = grid.move()
            if not can_still_move:
                break
        grid.turn(direction=direction)

    if last_steps:
        for _ in range(int(last_steps)):
            grid.move()
    if args.viz:
        grid.draw()
        cv2.waitKey(0)

    print(f"Final password: {grid.determine_password()}")


if __name__ == '__main__':
    day22_part1()
