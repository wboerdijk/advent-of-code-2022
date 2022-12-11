"""
Advent of code - day 10, part 2
(c) Wout Boerdijk
"""

from pathlib import Path
import argparse
import numpy as np


def day10_part2():
    """
    Prints the results for the day 10 part 2 riddle.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 10, part 2. Run "
                                                 "`python day10/day10_part2.py`. "
                                                 "Add `--with-white-spaces` for a clearer "
                                                 "print out.")
    parser.add_argument('--with-white-spaces', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        instructions = [line.strip() for line in file.readlines()]

    pixel_image = ''
    crt_row = ''
    sprite_pos = np.arange(1, 4)
    counter = 0
    for instruction in instructions:
        if counter % 40 == 0 and counter > 0 and crt_row != '':  # reset crt row
            pixel_image += crt_row + '\n'
            crt_row = ''

        if (counter % 40) + 1 in sprite_pos:
            crt_row += '#'
        else:
            crt_row += ' ' if args.with_white_spaces else '.'
        counter += 1

        if counter % 40 == 0 and counter > 0 and crt_row != '':  # reset crt row
            pixel_image += crt_row + '\n'
            crt_row = ''

        if instruction.startswith('addx'):
            if (counter % 40) + 1 in sprite_pos:
                crt_row += '#'
            else:
                crt_row += ' ' if args.with_white_spaces else '.'
            counter += 1
            sprite_pos += int(instruction.split(' ')[-1])

    print(f"Pixel image:\n\n{pixel_image}")


if __name__ == '__main__':
    day10_part2()
