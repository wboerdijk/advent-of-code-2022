"""
Advent of code - day 18
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path
import numpy as np


def cube_march(current_cubes, visited_cubes=None, invalid_cubes=None):
    """
    Simple floodfill algorithm to fill the cubes.
    :param current_cubes: (set) set of current cubes to investigate from
    :param visited_cubes: (set) set of already visited cubes
    :param invalid_cubes: (set) set of invalid cubes (border and given cubes)
    :return: (set) set of cubes that were filled
    """
    # get next cubes
    next_cubes = set()
    for coord_i, coord_j, coord_k in current_cubes:
        next_cubes.add((coord_i+1, coord_j, coord_k))
        next_cubes.add((coord_i-1, coord_j, coord_k))
        next_cubes.add((coord_i, coord_j+1, coord_k))
        next_cubes.add((coord_i, coord_j-1, coord_k))
        next_cubes.add((coord_i, coord_j, coord_k+1))
        next_cubes.add((coord_i, coord_j, coord_k-1))

    # remove invalid cubes
    next_cubes = next_cubes - invalid_cubes
    if visited_cubes:
        next_cubes = next_cubes - visited_cubes
    visited_cubes = current_cubes

    if next_cubes:
        visited_cubes = visited_cubes.union(cube_march(current_cubes=next_cubes,
                                                       visited_cubes=current_cubes,
                                                       invalid_cubes=invalid_cubes))
    return visited_cubes


def get_border_cubes(size):
    """
    Helper to get cube indices located at the border of a `size` large cube.
    :param size: (int) cube size
    :return: (set) set of cube coordinates
    """
    coords_a = np.tile(np.arange(size), size)
    coords_b = np.arange(size).repeat(repeats=size)

    coords = {(coord_a, coord_b, 0) for coord_a, coord_b in zip(coords_a, coords_b)}
    coords.update({(coord_a, coord_b, size-1) for coord_a, coord_b in zip(coords_a, coords_b)})
    coords.update({(coord_a, 0, coord_b) for coord_a, coord_b in zip(coords_a, coords_b)})
    coords.update({(coord_a, size-1, coord_b) for coord_a, coord_b in zip(coords_a, coords_b)})
    coords.update({(0, coord_a, coord_b) for coord_a, coord_b in zip(coords_a, coords_b)})
    coords.update({(size-1, coord_a, coord_b) for coord_a, coord_b in zip(coords_a, coords_b)})

    return coords


def get_cube_surface(cubes):
    """
    Returns the total visible cube surface area. Operation is based on the fact that adjacent cubes
    share one surface. Hence, for every adjacent cube pair, the total surface is reduced by 2.
    :param cubes: (np.array) array of cubes
    :return: (int) visible surface area
    """
    total_surfaces = 6 * cubes.shape[0]

    for i in range(cubes.shape[0]):
        for j in range(i+1, cubes.shape[0]):
            if np.abs(cubes[i] - cubes[j]).sum() == 1:
                total_surfaces -= 2

    return total_surfaces


def day18():
    """
    Prints the results for the two day 18 riddles.
    :return:
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--part-2', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        cubes = np.array([eval(line.strip()) for line in file.readlines()])

    if args.part_2:
        # idea is to do a floodfill outside the cubes, count the surface area like for part 1,
        # and subtract the outside surface
        # for this we first normalize the cubes
        # zero is the outside border, then comes the border where we do the floodfill
        # therefore, cubes have to start at 2
        cubes -= cubes.min()
        cubes += 2

        # this is the outmost layer of the cube
        # inside we do the floodfill
        outter_cube_size = cubes.max() - cubes.min() + 5
        invalid_cubes = get_border_cubes(size=outter_cube_size)
        invalid_cubes = invalid_cubes.union({(coord_i, coord_j, coord_k) for
                                             coord_i, coord_j, coord_k in cubes})

        # cube marching - floodfilling the second-outer layer
        cubes = cube_march(current_cubes={(1, 1, 1)}, visited_cubes=None,
                           invalid_cubes=invalid_cubes)
        cubes = np.stack([coord_i, coord_j, coord_k] for coord_i, coord_j, coord_k in cubes)

    surface_area = get_cube_surface(cubes=cubes)

    if args.part_2:
        surface_area -= ((outter_cube_size - 2) ** 2) * 6

    print(f"Surface area: {surface_area}")




if __name__ == '__main__':
    day18()
