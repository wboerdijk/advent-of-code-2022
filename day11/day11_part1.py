"""
Advent of code - day 11, part 1
(c) Wout Boerdijk
"""

from pathlib import Path
import numpy as np


class MonkeyGame:
    """
    Class representing a monkey game.
    """
    def __init__(self, monkeys):
        """
        Initializes a monkey game.
        :param monkeys: (list) list of monkeys
        """
        self.monkeys = monkeys
        self.worry_levels_per_round = []

    def play(self, num_rounds=1, decrease_worry_level=True):
        """
        Plays a certain number of rounds.
        :param num_rounds: (int) the number of rounds
        :param decrease_worry_level: (bool) whether to decrease the worry level
        :return:
        """
        for _ in range(num_rounds):
            for _, monkey in enumerate(self.monkeys):
                for _ in range(len(monkey.items_with_worry_level)):
                    item_with_worry_level, throw_to = monkey.examine_next_item(
                        decrease_worry_level=decrease_worry_level)
                    self.monkeys[throw_to].items_with_worry_level.append(item_with_worry_level)
            self.worry_levels_per_round.append([monkey.num_inspections for monkey in self.monkeys])

    def get_monkey_business(self):
        """
        Returns the monkey business, defined as the multiplication between the two most active
        monkeys.
        :return: (int) the monkey business
        """
        monkey_inspections = sorted([monkey.num_inspections for monkey in self.monkeys],
                                    reverse=True)
        return monkey_inspections[0] * monkey_inspections[1]


class Monkey:
    """
    Class representing a monkey.
    """
    def __init__(self, items_with_worry_level, operator, operand, test_dividend,
                 throw_to_if_test_true, throw_to_if_test_false):
        """
        Initializes a monkey.
        :param items_with_worry_level: (int) the worry level of an item
        :param operator: (str) the operator of the monkey's operation
        :param operand: (str/int) the operand of the monkey's operation
        :param test_dividend: (int) the divident for the monkey's test division
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
        if self.operator == '*':
            item *= self.operand if isinstance(self.operand, int) else item
        else:
            item += self.operand if isinstance(self.operand, int) else item
        self.num_inspections += 1
        if decrease_worry_level:
            item = np.floor(item / 3).astype(int)
        if item % self.test_dividend == 0:
            return item, self.throw_to_if_test_true
        return item, self.throw_to_if_test_false


def day11_part1():
    """
    Prints the results for the day 11 part 1 riddle.
    :return:
    """
    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]

    # parse lines to monkeys
    monkeys = []
    for monkey_line in range(0, len(lines), 7):
        items_with_worry_level = [int(starting_item) for starting_item in
                                  lines[monkey_line + 1].replace(',', '').split(' ')[2:]]
        operator, operand = lines[monkey_line + 2].split(' ')[-2:]
        test_dividend = int(lines[monkey_line + 3].split(' ')[-1])
        throw_to_if_test_true = int(lines[monkey_line + 4].split(' ')[-1])
        throw_to_if_test_false = int(lines[monkey_line + 5].split(' ')[-1])
        monkey = Monkey(items_with_worry_level=items_with_worry_level, operator=operator,
                        operand=operand, test_dividend=test_dividend,
                        throw_to_if_test_true=throw_to_if_test_true,
                        throw_to_if_test_false=throw_to_if_test_false)
        monkeys.append(monkey)

    monkey_game = MonkeyGame(monkeys=monkeys)
    monkey_game.play(num_rounds=20, decrease_worry_level=True)
    print(f"Monkey business after 20 rounds: {monkey_game.get_monkey_business()}")


if __name__ == '__main__':
    day11_part1()
