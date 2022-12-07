"""
Advent of code - day 5
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path


def lines_to_stack(lines):
    """
    Returns a stack given a list of lines.
    :param lines: list of strings
    :return: list of lists representing the stack
    """
    num_stacks = len([char for char in lines[-1].strip() if char != ' '])

    # create a list of lists representing the stacks and their crates
    stacks = [[] for _ in range(num_stacks)]

    # fill the stacks
    for line in lines[:-1][::-1]:
        crates = [line[x:x + 4][1:2] for x in range(0, len(line), 4)]
        for crate_idx, crate in enumerate(crates):
            if crate == ' ':
                continue
            stacks[crate_idx].append(crate)

    return stacks


def lines_to_commandos(lines):
    """
    Returns a stack given a list of lines.
    :param lines: list of strings
    :return: list of lists representing the commands
    """
    commandos = []
    for line in lines:
        _, howmany, _, move_from, _, move_to = line.strip().split(' ')
        commandos.append([int(howmany), int(move_from) - 1, int(move_to) - 1])
    return commandos


def day5():
    """
    Prints the results for the two day 2 riddles.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 5. Run "
                                                 "`python day5/day5.py` for the first part, "
                                                 "and `python day5/day5.py --part-2` for the "
                                                 "second part.")
    parser.add_argument('--part-2', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        data_lines = file.readlines()

    # get the line that splits the stack and the commandos
    split = [i for i, data_line in enumerate(data_lines) if data_line == '\n'][0]

    # transform lines to list of lists for easier processing
    stack = lines_to_stack(data_lines[:split])
    commandos = lines_to_commandos(data_lines[split + 1:])

    # go through all commandos
    for (howmany, move_from, move_to) in commandos:
        crates = stack[move_from][-howmany:]
        if not args.part_2:
            crates = crates[::-1]
        stack[move_from] = stack[move_from][:-howmany]
        stack[move_to].extend(crates)

    print(f"Final top crates: {''.join([sub_stack[-1] for sub_stack in stack])}")


if __name__ == '__main__':
    day5()
