"""
Advent of code - day 14
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path
import numpy as np
import cv2


def coords_to_filled_set(start_coords, end_coords):
    """
    Fills missing coordinate values and returns a set of filled coordinates.
    :param start_coords: (tuple) (i, j) start indices
    :param end_coords: (tuple) (i, j) end indices
    :return: (set) set of filled coordinates
    """
    coords = set()
    start_i = min(start_coords[0], end_coords[0])
    end_i = max(start_coords[0], end_coords[0])
    start_j = min(start_coords[1], end_coords[1])
    end_j = max(start_coords[1], end_coords[1])
    for coords_i in range(start_i, end_i + 1):
        for coords_j in range(start_j, end_j + 1):
            coords.add((coords_i, coords_j))
    return coords


def add_to_coords(coords, value=(0, 0)):
    """
    Adds a value to a set of coordinates.
    :param coords: (set) set of coordinates
    :param value: (tuple) (i, j) delta
    :return: (set) updated coordinate set
    """
    return {(coord[0] + value[0], coord[1] + value[1]) for coord in coords}


class Cave:
    """
    Class representing a cave for simulating falling sand.
    """
    def __init__(self, rock_coords, sand_origin_coords, with_ground_floor=False):
        """
        Initializes a cave instance.
        :param rock_coords: (set) set of rock coordinates
        :param sand_origin_coords: (set) sand origin coordinates
        :param with_ground_floor: (bool) optionally adds a ground floor for the second part of the
                                  riddle
        """
        rock_coords_arr = np.array(list(rock_coords))

        rock_coords_min_i, rock_coords_min_j = rock_coords_arr.min(axis=0)
        rock_coords_max_i, rock_coords_max_j = rock_coords_arr.max(axis=0)
        rock_coords_min_i = min(rock_coords_min_i, list(sand_origin_coords)[0][0])
        rock_coords_min_j = min(rock_coords_min_j, list(sand_origin_coords)[0][1])

        self.rock_coords = {(coords_i - rock_coords_min_i, coords_j - rock_coords_min_j) for
                            coords_i, coords_j in rock_coords}
        self.sand_origin_coords = {(list(sand_origin_coords)[0][0] - rock_coords_min_i,
                                    list(sand_origin_coords)[0][1] - rock_coords_min_j)}
        self.coords_max_i = rock_coords_max_i - rock_coords_min_i
        self.coords_max_j = rock_coords_max_j - rock_coords_min_j

        if with_ground_floor:
            self.add_ground_floor()

        self.sand_coords = set()
        self.valid_sand_coords = set()

        # draw the abyss border in any case, doesn't matter for the result
        self.abyss_border = self.get_abyss_border()

        self.width = 5
        self.offset = self.width
        self.initialize_grid()

    def add_ground_floor(self, offset=200):
        """
        Adds a ground floor of rocks to all already existing rocks.
        :param offset: (int) left and right offset. Could be lower than 200 (upper bound is the
                       maximum width).
        :return:
        """
        # shift all rock coords to the right
        self.rock_coords = add_to_coords(self.rock_coords, value=(0, offset))
        self.sand_origin_coords = add_to_coords(self.sand_origin_coords, value=(0, offset))
        floor_coord_min_j = -1
        floor_coord_max_j = self.coords_max_j + 2 * offset + 1
        for coord_j in range(floor_coord_min_j, floor_coord_max_j):
            self.rock_coords.update({(self.coords_max_i + 2, coord_j)})
        self.coords_max_i += 2
        self.coords_max_j += 2 * offset

    def get_abyss_border(self):
        """
        Creates a set of coordinates representing the abyss border located at the very left,
        bottom and right part.
        :return: (set) set of abyss coordinates
        """
        abyss_border = set()
        for coord_i in range(self.coords_max_i + 2):
            abyss_border.update({(coord_i, -1)})
            abyss_border.update({(coord_i, self.coords_max_j+1)})
        for coord_j in range(self.coords_max_j + 1):
            abyss_border.update({(self.coords_max_i + 1, coord_j)})

        return abyss_border

    def get_all_filled_coords(self):
        """
        Returns all coordinates filled with rock or sand.
        :return: (set) filled coordinates
        """
        return set().union(*[self.rock_coords, self.sand_origin_coords, self.sand_coords])

    def _get_symbol_for_drawing(self, symbol='cube', fill=255):
        """
        Helper to return a symbol for the interactive visualization.
        :param symbol: (str) one of ['cube', 'plus', 'diamond']
        :param fill: (int) grayscale strength
        :return: (np.array) 2d array representing the symbol
        """
        area = np.zeros((self.width, self.width), dtype=np.uint8)
        if symbol == 'cube':
            area += fill
        elif symbol == 'plus':
            middle = int(self.width / 2)
            area[1:-1, middle] = fill
            area[middle, 1:-1] = fill
        elif symbol == 'diamond':
            middle = int(self.width / 2)
            area[middle, middle] = fill
            kernel = np.ones((3, 3), dtype=np.uint8)
            kernel[0, 0] = 0
            kernel[0, 2] = 0
            kernel[2, 0] = 0
            kernel[2, 2] = 0
            area = cv2.dilate(area, kernel=kernel, iterations=middle)
        else:
            raise NotImplementedError
        return area

    def _get_drawing_pos(self, coord_i, coord_j):
        """
        Helper to return the bounding box coordinates of the position to draw.
        :param coord_i: (int) i-th coordinate
        :param coord_j: (int) j-th coordinatet
        :return: (tuple) tuple of ints representing the bounding box
        """
        start_i = self.offset+coord_i*self.width
        end_i = self.offset+coord_i*self.width+self.width
        start_j = self.offset+coord_j*self.width
        end_j = self.offset+coord_j*self.width+self.width
        return start_i, end_i, start_j, end_j

    def initialize_grid(self):
        """
        Initializes an empty 2d grid representing the cave. Draws rocks, the sand origin and the
        abyss.
        :return:
        """
        self.cave_grid = np.zeros((2*self.offset+self.coords_max_i*self.width+self.width,
                                   2*self.offset+self.coords_max_j*self.width+self.width),
                                  dtype=np.uint8)

        self.update_grid(grid=self.cave_grid, coords=self.rock_coords, symbol='cube')
        self.update_grid(grid=self.cave_grid, coords=self.sand_origin_coords, symbol='plus')
        self.update_grid(grid=self.cave_grid, coords=self.abyss_border, symbol='cube', fill=128)

    def update_grid(self, grid, coords, symbol, fill=255):
        """
        Updates the grid.
        :param grid: (np.array) 2d array representing the cave
        :param coords: (set) set of coordinates
        :param symbol: (str) symbol to use for plotting
        :param fill: (int) symbol fill value
        :return: (np.array) the updated grid
        """
        if grid is None:
            grid = self.cave_grid
        for (coord_i, coord_j) in coords:
            start_i, end_i, start_j, end_j = self._get_drawing_pos(coord_i=coord_i, coord_j=coord_j)
            grid[start_i:end_i, start_j:end_j] = self._get_symbol_for_drawing(symbol=symbol,
                                                                              fill=fill)
        return grid

    def visualize_cave_grid(self, delay=5):
        """
        Visualizes the cave grid.
        :param delay: (int) cv2.waitKey() delay
        :return:
        """
        grid = self.cave_grid.copy()
        grid = self.update_grid(grid=grid, coords=self.valid_sand_coords, symbol='diamond',
                                fill=128)
        cv2.imshow('cave grid', grid)
        cv2.waitKey(delay=delay)

    def check_if_inside_borders(self, coords):
        """
        Helper to check if coordinates are not in the abyss.
        :param coords: (set) set of coordinates
        :return: (bool) boolean indicating whether one of the coordinates touches the abyss.
        """
        assert len(coords) == 1
        coord_i, coord_j = list(coords)[0]
        return 0 <= coord_i <= self.coords_max_i and 0 <= coord_j <= self.coords_max_j

    def pour_sand(self, sand_coords=None, viz=False):
        """
        Pours one grain of sand and recursively updates until the sand is no longer moving.
        :param sand_coords: (set, None) optional sand coordinates. If None, will pour from the sand
                            origin
        :param viz: (bool) toggle visualization
        :return: (bool) boolean indicating whether it is still possible to pour new sand
        """
        if sand_coords is None:
            sand_coords = self.sand_origin_coords

        # get valid next coordinates
        down = add_to_coords(sand_coords, value=(1, 0))
        down_left = add_to_coords(sand_coords, value=(1, -1))
        down_right = add_to_coords(sand_coords, value=(1, 1))
        possible_sand_coords = {list(down)[0], list(down_left)[0], list(down_right)[0]}

        self.valid_sand_coords = possible_sand_coords.difference(self.get_all_filled_coords())

        # exit if the sand touches the abyss
        if self.valid_sand_coords.intersection(self.abyss_border):
            return False

        if viz:
            self.visualize_cave_grid(delay=50)

        # recursively go to the next position if there exists one
        if len(self.valid_sand_coords) != 0:
            if self.valid_sand_coords.intersection(down):
                return self.pour_sand(sand_coords=down, viz=viz)
            if self.valid_sand_coords.intersection(down_left):
                return self.pour_sand(sand_coords=down_left, viz=viz)
            return self.pour_sand(sand_coords=down_right, viz=viz)
        else:
            if sand_coords == self.sand_origin_coords:
                return False
            self.sand_coords.update(sand_coords)
            if viz:
                self.update_grid(grid=None, coords=sand_coords, symbol='diamond', fill=255)
                self.visualize_cave_grid(delay=50)
            return True


def day14():
    """
    Prints the results for the two day 14 riddles.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 14. Run "
                                                 "`python day14/day14.py` for the first part, "
                                                 "and `python day14/day14.py --part-2` for the "
                                                 "second part. Add `--viz` for an interactive "
                                                 "visualization.")
    parser.add_argument('--part-2', default=False, action='store_true')
    parser.add_argument('--viz', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        rock_lines = [line.strip() for line in file.readlines()]

    rock_starts, rock_ends, rock_coords = [], [], set()
    for rock_line in rock_lines:
        rock_line = [rock_segment.split(',') for rock_segment in rock_line.split(' -> ')]
        rock_line = [[int(rock_x), int(rock_y)] for (rock_x, rock_y) in rock_line]
        for index in range(len(rock_line) - 1):
            rock_coords.update(coords_to_filled_set(rock_line[index][::-1],
                                                    rock_line[index + 1][::-1]))
            rock_starts.append(rock_line[index])
            rock_ends.append(rock_line[index + 1])

    # initialize a cave
    cave = Cave(rock_coords=rock_coords, sand_origin_coords={(0, 500)},
                with_ground_floor=args.part_2)

    # pour sand until nothing else is moving
    while True:
        if not cave.pour_sand(viz=args.viz):
            break

    if args.viz:
        cv2.waitKey(0)

    print(f"Resting sand units: {len(cave.sand_coords) + (1 if args.part_2 else 0)}")


if __name__ == '__main__':
    day14()
