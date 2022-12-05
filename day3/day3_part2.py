"""
Advent of code - day 3, part 2
(c) Wout Boerdijk
"""

from pathlib import Path


def day3_part2():
    """
    Prints the results for the day 3 part 2 riddle.
    :return:
    """
    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        data_lines = file.readlines()

    data_lines = [data_line.strip() for data_line in data_lines]
    data_lines = [data_lines[x:x + 3] for x in range(0, len(data_lines), 3)]

    total_points = 0
    for data_line in data_lines:
        intersection = set(data_line[0]).intersection(data_line[1]).intersection(data_line[2])
        intersection = list(intersection)[0]
        if intersection.isupper():
            total_points += ord(intersection) - 65 + 27
        else:
            total_points += ord(intersection) - 97 + 1

    print(total_points)


if __name__ == '__main__':
    day3_part2()
