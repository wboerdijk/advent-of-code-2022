"""
Advent of code - day 8
(c) Wout Boerdijk
"""

from pathlib import Path
import numpy as np


def get_visible_trees(tree_line):
    """
    Returns the visible indices given a tree line.
    :param tree_line: (np.array) single tree line
    :return: (list) visible trees in binary form
    """
    visible_trees = [1]
    curr_max = tree_line[0]
    for tree in tree_line[1:]:
        if tree > curr_max:
            visible_trees.append(1)
            curr_max = tree
        else:
            visible_trees.append(0)
    return visible_trees


def day8_part1():
    """
    Prints the results for the day 8 part 1 riddle.
    :return:
    """
    trees = np.genfromtxt(Path(__file__).parent.resolve().joinpath('input.txt'),
                          delimiter=1, dtype=int)

    # looking from left
    visible_from_left = np.zeros_like(trees)
    for num_line, tree_line in enumerate(trees):
        visible_from_left[num_line] = get_visible_trees(tree_line=tree_line)

    # looking from right
    visible_from_right = np.zeros_like(trees)
    for num_line, tree_line in enumerate(trees):
        visible_from_right[num_line] = get_visible_trees(tree_line=tree_line[::-1])[::-1]

    # looking from top
    visible_from_top = np.zeros_like(trees)
    for num_line in range(trees.shape[1]):
        visible_from_top[:, num_line] = get_visible_trees(tree_line=trees[:, num_line])

    # looking from bottom
    visible_from_bottom = np.zeros_like(trees)
    for num_line in range(trees.shape[1]):
        visible_from_bottom[:, num_line] = get_visible_trees(
            tree_line=trees[:, num_line][::-1])[::-1]

    total_visible = visible_from_left + visible_from_right + visible_from_top + visible_from_bottom
    total_visible[total_visible >= 1] = 1
    print(f"Visible trees: {total_visible.sum()}")


if __name__ == '__main__':
    day8_part1()
