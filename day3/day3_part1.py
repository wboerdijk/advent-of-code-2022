"""
Advent of code - day 3, part 1
(c) Wout Boerdijk
"""

from pathlib import Path


def day3_part1():
    """
    Prints the results for the day 3 part 1 riddle.
    :return:
    """
    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        data_lines = file.readlines()

    data_lines = [data_line.strip() for data_line in data_lines]

    total_points = 0
    for data_line in data_lines:
        part1, part2 = data_line[:int(len(data_line) / 2)], data_line[int(len(data_line) / 2):]
        intersection = set(part1).intersection(part2)
        intersection = list(intersection)[0]
        if intersection.isupper():
            total_points += ord(intersection) - 65 + 27
        else:
            total_points += ord(intersection) - 97 + 1

    print(f"Total points: {total_points}")


if __name__ == '__main__':
    day3_part1()
