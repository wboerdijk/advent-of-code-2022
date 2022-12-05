"""
Advent of code - day 4
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path


def day4():
    """
    Prints the results for the day 3 part 1 riddle.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 4. Run "
                                                 "`python day4/day4.py` for the first part, "
                                                 "and `python day4/day4.py --part-2` for the "
                                                 "second part.")
    parser.add_argument('--part-2', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        data_lines = file.readlines()

    data_lines = [data_line.strip() for data_line in data_lines]

    total_count = 0
    for data_line in data_lines:
        set1, set2 = data_line.split(',')
        set1_start, set1_end = set1.split('-')
        set2_start, set2_end = set2.split('-')
        list1 = list(range(int(set1_start), int(set1_end) + 1))
        list2 = list(range(int(set2_start), int(set2_end) + 1))

        intersection = set(list1).intersection(list2)

        if args.part_2 and len(intersection) > 0:
            total_count += 1
        elif set(list1).issubset(intersection) or set(list2).issubset(intersection):
            total_count += 1

    print(f"Total count: {total_count}")


if __name__ == '__main__':
    day4()
