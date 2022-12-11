"""
Advent of code - day 10, part 1
(c) Wout Boerdijk
"""

from pathlib import Path


def day10_part1():
    """
    Prints the results for the day 10 part 1 riddle.
    :return:
    """
    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        instructions = [line.strip() for line in file.readlines()]

    values_during, values_after = [1], [1]

    for instruction in instructions:
        if instruction == 'noop':
            values_during.append(values_after[-1])
            values_after.append(values_after[-1])
        else:
            value_to_add = int(instruction.split(' ')[-1])
            # addx takes two steps
            values_during.append(values_after[-1])
            values_after.append(values_after[-1])
            values_during.append(values_after[-1])
            values_after.append(values_after[-1] + value_to_add)

    total_signal_strength = 0
    for position in range(20, 221, 40):
        total_signal_strength += position * values_during[position]

    print(f"Total signal strength: {total_signal_strength}")


if __name__ == '__main__':
    day10_part1()
