"""
Advent of code - day 1
(c) Wout Boerdijk
"""

import argparse
import pathlib


def day1():
    """
    Prints the results for the two day 1 riddles.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 1. Run "
                                                 "`python day1/day1.py` for the first part, and "
                                                 "`python day1/day1.py --top-k 3` "
                                                 "for the second part.")
    parser.add_argument('--top-k', type=int, default=1)
    args = parser.parse_args()
    assert args.top_k > 0, f"`top-k` needs to be larger than 0, got {args.top_k}!"

    # load the data
    with open(pathlib.Path(__file__).parent.resolve().joinpath('input.txt'), 'r',
              encoding='utf-8') as file:
        calory_lines = file.readlines()

    # sweep through the list and add the values per elf
    calories_per_elf = []
    current_calories = 0
    for calory_line in calory_lines:
        if calory_line != '\n':
            current_calories += int(calory_line.strip())
        else:
            calories_per_elf.append(current_calories)
            current_calories = 0

    calories_per_elf = sorted(calories_per_elf, reverse=True)
    print(f"Maximum calories (k={args.top_k}): "
          f"{sum(calories_per_elf[:min(len(calories_per_elf), args.top_k)])}")


if __name__ == '__main__':
    day1()
