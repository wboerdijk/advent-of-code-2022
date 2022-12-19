"""
Advent of code - day 15, part 2
(c) Wout Boerdijk
"""

from pathlib import Path
import numpy as np


def manhattan_distance(coords_a, coords_b):
    """
    Calculates the manhattan distance between a pair of coordinates.
    :param coords_a: (tuple) first pair of coordinates
    :param coords_b: (tuple) second pair of coordinates
    :return: (int) the manhattan distance between the two coordinates
    """
    return abs(coords_a[0] - coords_b[0]) + abs(coords_a[1] - coords_b[1])


def select_coords_larger_than_distance(coords, center, distance):
    """
    Function to select coordinates that are further away (in terms of the manhattan distance)
    to a center than a certain distance provided.
    :param coords: (np.array) array of coordinates
    :param center: (np.array) center coordinates
    :param distance: (int) distance to be evaluated
    :return: (np.array) the coordinates which are further away from the center than the distance
             provided
    """
    return coords[np.where(np.abs(coords - center).sum(axis=-1) > distance)]


def get_border_kernel_set(center_coords, distance, max_size):
    """
    Returns a set of coordinates which form the border outside the (manhattan) distance.
    Coordinates smaller than 0 and larger than `max_size` are discarded.
    :param center_coords: (set) the center coordinates
    :param distance: (int) the distance up to the border
    :param max_size: (int) maximum size of coordinate values
    :return: (set) the coordinates forming the border outside the given distance
    """
    coords_i, coords_j = center_coords

    descending_i = np.arange(coords_i - distance, coords_i + 1)
    descending_j = np.arange(coords_j, coords_j + distance + 1)

    top_to_right = set(zip(descending_i, descending_j))
    left_to_top = set(zip(descending_i[::-1], descending_j - distance))
    left_to_bot = set(zip(descending_i + distance, descending_j - distance))
    bot_to_right = set(zip(descending_i[::-1] + distance, descending_j))

    top_to_right.update(left_to_top)
    top_to_right.update(left_to_bot)
    top_to_right.update(bot_to_right)

    valid_coords = {(coord_i, coord_j) for coord_i, coord_j in top_to_right if
                    0 <= coord_i <= max_size and 0 <= coord_j <= max_size}

    return valid_coords


def day15_part2():
    """
    Prints the results for the day 15 part 2 riddle.
    :return:
    """
    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]

    # format the lines
    all_sensor_coords, all_beacon_coords, distances = [], [], []
    for line in lines:
        line = line.replace('x=', '').replace('y=', '').replace(',', '').replace(':', '').split(' ')
        all_sensor_coords.append((int(line[3]), int(line[2])))
        all_beacon_coords.append((int(line[9]), int(line[8])))
        distances.append(manhattan_distance(all_sensor_coords[-1], all_beacon_coords[-1]))

    size = 4000000

    # idea is to first get the by one (manhattan) distance extended border of the sensors
    # these are all valid positions for the distress beacons
    possible_beacon_spots = set()
    for sensor_coords, distance in zip(all_sensor_coords, distances):
        possible_beacon_spots.update(get_border_kernel_set(center_coords=sensor_coords,
                                                           distance=distance+1, max_size=size-1))

    # then, iterate through all sensors, and discard all possible beacon spots that are
    # within the selected distance of that sensor
    # only one spot must remain - the distress beacon
    possible_beacon_spots = np.array(list(possible_beacon_spots))
    for sensor_coords, distance in zip(all_sensor_coords, distances):
        possible_beacon_spots = select_coords_larger_than_distance(possible_beacon_spots,
                                                                   sensor_coords, distance)

    assert len(possible_beacon_spots) == 1
    y_coord, x_coord = list(possible_beacon_spots)[0]
    print(f"Tuning frequency of the distress beacon: {x_coord * 4000000 + y_coord}")


if __name__ == '__main__':
    day15_part2()
