"""
Advent of code - day 6
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path


def day6():
    """
    Prints the results for the two day 2 riddles.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 6. Run "
                                                 "`python day6/day6.py` for the first part, "
                                                 "and `python day6/day6.py --part-2` for the "
                                                 "second part.")
    parser.add_argument('--part-2', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        data_line = file.readlines()[0].strip()

    marker_length = 14 if args.part_2 else 4

    for i in range(len(data_line)):
        if len(set(data_line[i:i+marker_length])) == marker_length:
            print(f"Start-of-{'message' if args.part_2 else 'packet'}-marker: {i + marker_length}")
            break


if __name__ == '__main__':
    day6()
