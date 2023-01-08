"""
Advent of code - day 17, part 1
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path
import numpy as np
import cv2


class Rock:
    """
    Class representing a rock.
    """
    def __init__(self, shape=1, offset=4):
        """
        Initializes a rock.
        :param shape: (int) integer mapping to the corresponding shape
        :param offset: (int) integer describing the offset from the floor
        """
        if shape == 1:
            self.indices = {(0, 3), (0, 4), (0, 5), (0, 6)}
        elif shape == 2:
            self.indices = {(0, 4), (1, 3), (1, 4), (1, 5), (2, 4)}
        elif shape == 3:
            self.indices = {(2, 5), (1, 5), (0, 3), (0, 4), (0, 5)}
        elif shape == 4:
            self.indices = {(0, 3), (1, 3), (2, 3), (3, 3)}
        else:
            self.indices = {(0, 3), (0, 4), (1, 3), (1, 4)}
        self.indices = {(index_i + offset, index_j) for index_i, index_j in self.indices}

    def move(self, direction='<'):
        """
        Moves the indices of a rock to the left or to the right.
        :param direction: (str) one of ['<', '>'] indicating left or right movement
        """
        if direction == '<':
            self.indices = {(index_i, index_j - 1) for index_i, index_j in self.indices}
        elif direction == '>':
            self.indices = {(index_i, index_j + 1) for index_i, index_j in self.indices}
        elif direction == 'down':
            self.indices = {(index_i - 1, index_j) for index_i, index_j in self.indices}
        else:
            self.indices = {(index_i + 1, index_j) for index_i, index_j in self.indices}


def max_from_set(set_of_coords, dim=0):
    """
    Helper to return the maximum value from a set of coordinates.
    :param set_of_coords: (set) set of 2d coordinates
    :param dim: (int) integer specifying x or y dimension
    """
    return np.array(list(set_of_coords))[:, dim].max() if len(set_of_coords) != 0 else 0


def min_from_set(set_of_coords, dim=0):
    """
    Helper to return the minimum value from a set of coordinates.
    :param set_of_coords: (set) set of 2d coordinates
    :param dim: (int) integer specifying x or y dimension
    """
    return np.array(list(set_of_coords))[:, dim].min() if len(set_of_coords) != 0 else 0


class Tower:
    """
    Class representing a tower.
    """
    def __init__(self, movements):
        """
        Initializes a tower structure.
        :param movements: (str) string representing consecutive left and right motions
        """
        self.movements = movements
        self.movement_index = 0
        self.floor = {(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8)}
        self.left_wall = {(1, 0), (2, 0), (3, 0)}
        self.right_wall = {(1, 8), (2, 8), (3, 8)}
        self.stopped_rocks = set()
        self.next_rock_index = 1

    def add_rock(self):
        """
        Adds one rock to the structure.
        """
        rock = Rock(shape=self.next_rock_index, offset=max_from_set(self.stopped_rocks) + 4)
        self._update_rock_index()

        self._add_wall(height=max_from_set(rock.indices, dim=0))

        # move
        self.move(rock)

    def get_all_static_parts(self):
        """
        Returns all static coordinate indices.
        """
        static_parts = self.floor.union(self.left_wall)
        static_parts = static_parts.union(self.right_wall)
        static_parts = static_parts.union(self.stopped_rocks)
        return static_parts

    def _invert_lr(self, direction='<'):
        """
        Helper to invert the direction.
        """
        if direction == '<':
            return '>'
        return '<'

    def move(self, rock):
        """
        Moves a rock to the next direction if possible, and then downwards if possible.
        """
        # first, move left / right
        rock.move(self.movements[self.movement_index])

        # if intersecting: move back
        if rock.indices.intersection(self.get_all_static_parts()):
            rock.move(self._invert_lr(direction=self.movements[self.movement_index]))

        # go to next motion
        self._update_movement_index()

        # then, move down
        rock.move(direction='down')
        if rock.indices.intersection(self.floor.union(self.stopped_rocks)):
            rock.move(direction='up')
            self.stopped_rocks.update(rock.indices)
        else:
            self.move(rock=rock)

    def cut_off(self):
        """
        Cuts off the structure based on a simple floodfill to reduce computation time.
        """
        floodfilled_tiles = self.floodfill()
        min_height = min_from_set(floodfilled_tiles)
        if min_height > 0:
            # remove walls and static rocks below min_height
            self.stopped_rocks = {(coord_i, coord_j) for coord_i, coord_j in self.stopped_rocks if coord_i >= min_height}
            self.left_wall = {(coord_i, coord_j) for coord_i, coord_j in self.left_wall if coord_i >= min_height}
            self.right_wall = {(coord_i, coord_j) for coord_i, coord_j in self.right_wall if coord_i >= min_height}
            self.floor = {(min_height - 1, coord_j) for coord_i, coord_j in self.floor}

    def _add_wall(self, height):
        """
        Helper to add walls.
        :param height: (int) the height of the wall
        """
        current_wall_height = max_from_set(self.left_wall, dim=0)
        for height_to_add in range(current_wall_height, height + 1):
            self.left_wall.add((height_to_add, 0))
            self.right_wall.add((height_to_add, 8))

    def _update_rock_index(self):
        """
        Helper to update the rock type indices. Resets if through all different types.
        """
        self.next_rock_index += 1
        if self.next_rock_index == 6:
            self.next_rock_index = 1

    def _update_movement_index(self):
        """
        Helper to update the movement indices. Resets if exceeding the string length.
        """
        self.movement_index += 1
        if self.movement_index >= len(self.movements):
            self.movement_index = 0

    def visualize(self):
        """
        Helper to visualize the rock dropping process.
        """
        size = 5
        max_height = max_from_set(self.left_wall, dim=0) + 1
        min_height = min_from_set(self.left_wall, dim=0) - 1
        height = max_height - min_height
        grid = np.zeros((size*height, size*9), dtype=np.uint8)

        self.update_grid(grid=grid, coords=self.stopped_rocks, symbol='hash', height_offset=min_height)
        self.update_grid(grid=grid, coords=self.left_wall, symbol='|', height_offset=min_height)
        self.update_grid(grid=grid, coords=self.right_wall, symbol='|', height_offset=min_height)
        self.update_grid(grid=grid, coords=self.floor, symbol='-', height_offset=min_height)

        cv2.imshow('grid', np.flipud(grid))
        cv2.waitKey(10)

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

    def _get_symbol_for_drawing(self, size=5, symbol='|', fill=255):
        """
        Helper to return a symbol for the interactive visualization.
        :param symbol: (str) one of ['cube', 'plus', 'diamond']
        :param fill: (int) grayscale strength
        :return: (np.array) 2d array representing the symbol
        """
        area = np.zeros((size, size), dtype=np.uint8)
        if symbol == '|':
            area[1:-1, 2] = fill
        elif symbol == '-':
            area[2, 1:-1] = fill
        elif symbol == 'hash':
            area[1] = fill
            area[3] = fill
            area[:, 1] = fill
            area[:, 3] = fill
        else:
            raise NotImplementedError
        return area

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

    def floodfill(self, flooded_tiles=None, previous_tiles=None):
        """
        Performs simple bottom-up floodfill to cut-off the tower.
        :param flooded_tiles: (set, None) set of tiles; if None, will initialize flooded tiles
        :param previous_tiles: (set, None) set of previous tiles, if available
        """
        if flooded_tiles is None:
            flooded_tiles = {(max_from_set(self.left_wall), 3)}
            previous_tiles = {}

        new_tiles = set()
        for coord_i, coord_j in flooded_tiles:
            # get next valid tiles
            new_tiles.add((coord_i, coord_j - 1))
            new_tiles.add((coord_i - 1, coord_j))
            new_tiles.add((coord_i, coord_j + 1))

        new_tiles = new_tiles - self.get_all_static_parts()
        if previous_tiles:
            new_tiles = new_tiles - previous_tiles
        previous_tiles = flooded_tiles

        if new_tiles:
            previous_tiles = previous_tiles.union(self.floodfill(flooded_tiles=new_tiles - self.get_all_static_parts(), previous_tiles=previous_tiles))
        return previous_tiles


def day17_part1():
    """
    Prints the results for the day 17 part 1 riddle.
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 17, part 1. Run "
                                                 "`python day17/day17_part1.py`. "
                                                 "Add `--viz` for a visualization.")
    parser.add_argument('--viz', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('debug.txt'), 'r', encoding='utf-8') as file:
        movements = file.readlines()[0]

    tower = Tower(movements=movements)

    for num_rock in range(2022):
        tower.add_rock()
        if args.viz:
            tower.visualize()
        if num_rock != 0 and num_rock % 1000 == 0:
            tower.cut_off()

    print(f"Current tower height: {max_from_set(tower.stopped_rocks)}")


if __name__ == '__main__':
    day17_part1()
