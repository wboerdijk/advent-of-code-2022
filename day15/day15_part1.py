"""
Advent of code - day 15, part 1
(c) Wout Boerdijk
"""

from pathlib import Path


def manhattan_distance(coords_a, coords_b):
    """
    Calculates the manhattan distance between a pair of coordinates.
    :param coords_a: (tuple) first pair of coordinates
    :param coords_b: (tuple) second pair of coordinates
    :return: (int) the manhattan distance between the two coordinates
    """
    return abs(coords_a[0] - coords_b[0]) + abs(coords_a[1] - coords_b[1])


def get_kernel_coords_in_row(center_coords, distance, row):
    """
    Returns a set of coordinates forming a diamond kernel around the center.
    :param center_coords: (tuple) center of the kernel
    :param distance: (int) kernel size
    :return: (set) kernel coordinates
    """
    kernel_coords = set()
    # form a square kernel first for convenience
    for coord_j in range(center_coords[1] - distance, center_coords[1] + distance + 1):
        if manhattan_distance(center_coords, (row, coord_j)) <= distance:
            kernel_coords.add((row, coord_j))
    return kernel_coords


def day15_part1():
    """
    Prints the results for the day 15 part 1 riddle.
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

    # define the target line
    target_row = 2000000
    valid_coords = set()
    for sensor_coords, distance in zip(all_sensor_coords, distances):
        valid_coords.update(get_kernel_coords_in_row(center_coords=sensor_coords, distance=distance,
                                                     row=target_row))

    valid_coords = valid_coords - set(all_sensor_coords)
    valid_coords = valid_coords - set(all_beacon_coords)

    print(f"Number of positions that cannot contain a beacon (y=2000000)): {len(valid_coords)}")


if __name__ == '__main__':
    day15_part1()
