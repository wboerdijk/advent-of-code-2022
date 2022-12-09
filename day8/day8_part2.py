"""
Advent of code - day 8, part 2
(c) Wout Boerdijk
"""

from pathlib import Path
import numpy as np


def get_scenic_score(trees, i, j):
    """
    Returns the scenic score given an array of trees and the indices of a tree.
    :param trees: (np.array) 2d array of trees
    :param i: (int) column index
    :param j: (int) row index
    :return: (int) scenic score of tree at [i, j]
    """
    scenic_score = 1
    curr_score = 0

    # look left
    for _j in range(j-1, -1, -1):
        curr_score += 1
        if trees[i, _j] >= trees[i, j] or _j == 0:
            scenic_score *= curr_score
            curr_score = 0
            break

    # look right
    for _j in range(j+1, trees.shape[1]):
        curr_score += 1
        if trees[i, _j] >= trees[i, j] or _j == trees.shape[1] - 1:
            scenic_score *= curr_score
            curr_score = 0
            break

    # look up
    for _i in range(i-1, -1, -1):
        curr_score += 1
        if trees[_i, j] >= trees[i, j] or _i == 0:
            scenic_score *= curr_score
            curr_score = 0
            break

    # look down
    for _i in range(i+1, trees.shape[0]):
        curr_score += 1
        if trees[_i, j] >= trees[i, j] or _i == trees.shape[0] - 1:
            scenic_score *= curr_score
            break

    return scenic_score


def day8_part2():
    """
    Prints the results for the day 8 part 2 riddle.
    :return:
    """
    trees = np.genfromtxt(Path(__file__).parent.resolve().joinpath('input.txt'),
                          delimiter=1, dtype=int)
    scenic_scores = np.zeros_like(trees)

    for i in range(1, trees.shape[0] - 1):
        for j in range(1, trees.shape[1] - 1):
            scenic_scores[i, j] = get_scenic_score(trees, i, j)

    print(f"Highest scenic score: {scenic_scores.max()}")


if __name__ == '__main__':
    day8_part2()
