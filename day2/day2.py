"""
Advent of code - day 2
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path


def determine_outcome(move1: str, move2: str) -> int:
    """
    Determines a rock-paper-scissor outcome.
    :param move1: first move ('A', 'B', 'C)
    :param move2: opponent move ('X', 'Y', 'Z')
    :return: outcoming points (0: loss, 3: draw, 6: win)
    """
    # convert to ints to make calculation easier
    move1 = ord(move1)
    move2 = ord(move2) - 23

    # draw
    if move1 == move2:
        return 3

    # win
    if move1 - move2 in [-1, 2]:
        return 6

    # loss
    if move1 - move2 in [1, -2]:
        return 0

    raise NotImplementedError(f"No computation for {move1}/{move2}!")


def outcome_to_move(move1: str, outcome: str) -> str:
    """
    Converts an outcome to a move.
    :param move1: the first move
    :param outcome: a single character ('X', 'Y', 'Z') denoting the outcome
    :return: the move to achieve the desired outcome
    """

    move1 = ord(move1)

    # lose
    if outcome == 'X':
        move2 = move1 - 1
        if move2 == 64:
            move2 = 67

    # draw
    elif outcome == 'Y':
        move2 = move1

    # win
    else:
        move2 = move1 + 1
        if move2 == 68:
            move2 = 65

    # add 23 to make it compatible with the first part
    return chr(move2 + 23)


def day2():
    """
    Prints the results for the two day 2 riddles.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 2. Run "
                                                 "`python day2/day2.py` for the first part, "
                                                 "and `python day2/day2.py --part-2` for the "
                                                 "second part.")
    parser.add_argument('--part-2',  default=False, action='store_true')
    args = parser.parse_args()

    # load the data
    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        rps_lines = file.readlines()

    # add points based on results
    total_points = 0
    for rps_line in rps_lines:
        opponent_move, your_move = rps_line.strip().split(' ')

        if args.part_2:
            your_move = outcome_to_move(opponent_move, your_move)

        total_points += ord(your_move) - 87 + determine_outcome(move1=opponent_move,
                                                                move2=your_move)

    print(f"Points earned: {total_points}")


if __name__ == '__main__':
    day2()
