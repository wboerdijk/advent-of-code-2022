"""
Advent of code - day 11
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path
import numpy as np


class MonkeyGame:
    """
    A class representing a monkey game.
    """
    def __init__(self, monkeys):
        """
        Initializes a monkey game instance.
        :param monkeys: (list) list of Monkey objects
        """
        self.monkeys = monkeys

    def play(self, num_rounds=1, decrease_worry_level=True):
        """
        Plays the monkey game for num_rounds.
        :param num_rounds: (int) number of rounds to play
        :param decrease_worry_level: (bool) whether to decrease the worry level
        :return:
        """
        for _ in range(num_rounds):
            for _, monkey in enumerate(self.monkeys):
                self.get_monkey_business()
                for num_item in range(len(monkey.items_with_worry_level)):
                    item_with_worry_level, throw_to = monkey.examine_next_item(decrease_worry_level=decrease_worry_level)
                    self.monkeys[throw_to].items_with_worry_level.append(item_with_worry_level)

    def get_monkey_business(self):
        """
        Calculates the monkey business, i.e. multiplies the two highest monkey inspection values.
        :return: 
        """
        monkey_inspections = sorted([monkey.num_inspections for monkey in self.monkeys], reverse=True)
        return monkey_inspections[0] * monkey_inspections[1]


class WorryLevelItem:
    """
    Class representing a worry level item.
    Idea is to represent the worry level as a multiple of the dividends' products, and some rest.
    To not reach similar high levels with the multiplying factor, it is represented as a binary power.
    Note that this approach works with arbitrary (also non-primary) dividends.
    """
    def __init__(self, initial_worry_level, dividends=[3, 13, 2, 11, 19, 17, 5, 7]):
        """
        Initializes a worry level item instance.
        :param initial_worry_level: (int) initial worry level
        :param dividends: (list) list of ints representing the dividents of the test cases
        """
        self.dividends = dividends
        self.rest = initial_worry_level
        self._has_prime_factors = False
        self._prime_initialized = False
        self.bin_pows = 0
        self.multiplier = 0

    def multiplier_to_bin_pows(self):
        """
        Helper to parse the multiplier to a binary-power representation - otherwise the multiplier would increase dramatically.
        :return:
        """
        bin_pows = np.floor(np.log2(self.multiplier))
        self.multiplier = self.multiplier - np.power(2, bin_pows)
        self.bin_pows += bin_pows

    def get_worry_level(self):
        """
        Returns the current worry level. Intended only for the first part of the riddle, since for the
        second part the numbers become too large.
        :return:
        """
        return np.prod(self.dividends) * (np.power(2, self.bin_pows - 1) if self.bin_pows != 0 else 0) * self.multiplier + self.rest

    def mul(self, factor):
        """
        Helper to multiply the current worry level with an integer, or with itself.
        :param factor: (int, str) integer to multiply the current worry level with, or 'old' indicating a multiplication with itself
        :return:
        """
        if isinstance(factor, int):
            self.rest *= factor
        else:
            self.rest *= self.rest

    def add(self, summand):
        """
        Helper to add an integer to the current worry level.
        :param summand: (int) the integer to add to the current worry level.
        :return:
        """
        self.rest += summand

    def div_test(self, dividend):
        """
        Helper to execute the given test case.
        :param dividend: (int) value to divide the current worry level by
        :return: (bool) whether the test was successful
        """
        return self.rest % dividend == 0

    def replace_with_dividend_factors(self):
        """
        Replaces the current rest with a multiple of the dividends' products.
        :return:
        """
        if self.rest >= np.prod(self.dividends):
            self.multiplier += np.floor(self.rest / np.prod(self.dividends)).astype(int)
            self.rest = self.rest % np.prod(self.dividends)


class Monkey:
    """
    Class representing a monkey.
    """
    def __init__(self, items_with_worry_level, operator, operand, test_dividend, throw_to_if_test_true, throw_to_if_test_false):
        """
        Initializes a monkey instance.
        :param items_with_worry_level: (list) list of ints representing the worry level of the monkey's items.
        :param operator: (str) one of '*', '+' representing the operation the monkey does.
        :param operand: (int, str) int for the operation or 'old' indicating a multiplication with itself.
        :param test_dividend: (int) integer for the test division
        :param throw_to_if_test_true: (int) id of the monkey to throw to in case the test is true
        :param throw_to_if_test_false: (int) id of the monkey to throw to in case the test is false
        """
        self.items_with_worry_level = items_with_worry_level
        self.operator = operator
        self.operand = int(operand) if operand != 'old' else operand
        self.test_dividend = test_dividend
        self.throw_to_if_test_true = throw_to_if_test_true
        self.throw_to_if_test_false = throw_to_if_test_false
        self.num_inspections = 0

    def examine_next_item(self, decrease_worry_level=True):
        """
        Examines the next item in the list.
        :param decrease_worry_level: (bool) whether to decrease the worry level
        :return: (int, int) tuple containing the worry level of an item and the index of the monkey
                 to throw to
        """
        item = self.items_with_worry_level.pop(0)

        # perform the operation
        if self.operator == '*':
            item.mul(self.operand)
        else:
            item.add(self.operand)

        # increment number of inspections
        self.num_inspections += 1

        if not decrease_worry_level:
            # decrease the multiplying factor, if possible
            item.replace_with_dividend_factors()

        # decrease the worry level (part 1)
        if decrease_worry_level:
            worry_level = item.get_worry_level()
            worry_level = np.floor(worry_level / 3).astype(int)
            item = WorryLevelItem(initial_worry_level=worry_level)

        # perform the test case
        if item.div_test(self.test_dividend):  # simple look-up since the test_dividends are all prime numbers
            return item, self.throw_to_if_test_true
        return item, self.throw_to_if_test_false


def day11():
    """
    Prints the results for the two day 11 riddles.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 11. Run "
                                                 "`python day11/day11.py` for the first part, "
                                                 "and `python day11/day11.py --part-2` for the "
                                                 "second part.")
    parser.add_argument('--part-2', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]

    # parse lines to monkeys
    monkeys = []
    for monkey_line in range(0, len(lines), 7):
        items_with_worry_level = [int(starting_item) for starting_item in lines[monkey_line + 1].replace(',', '').split(' ')[2:]]
        items_with_worry_level = [WorryLevelItem(item_with_worry_level) for item_with_worry_level in items_with_worry_level]
        operator, operand = lines[monkey_line + 2].split(' ')[-2:]
        test_dividend = int(lines[monkey_line + 3].split(' ')[-1])
        throw_to_if_test_true = int(lines[monkey_line + 4].split(' ')[-1])
        throw_to_if_test_false = int(lines[monkey_line + 5].split(' ')[-1])
        monkey = Monkey(items_with_worry_level=items_with_worry_level, operator=operator, operand=operand, test_dividend=test_dividend, throw_to_if_test_true=throw_to_if_test_true, throw_to_if_test_false=throw_to_if_test_false)
        monkeys.append(monkey)

    # initialize a monkey game, and play
    monkey_game = MonkeyGame(monkeys=monkeys)
    num_rounds = 10000 if args.part_2 else 20
    monkey_game.play(num_rounds=num_rounds, decrease_worry_level=not args.part_2)

    print(f"Monkey business after {num_rounds} rounds: {monkey_game.get_monkey_business()}")


if __name__ == '__main__':
    day11()
