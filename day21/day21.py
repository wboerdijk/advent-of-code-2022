"""
Advent of code - day 21
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path


def search_for_monkey(root_monkey):
    """
    Recursive search for the monkey `humn`, returns True if found else False.
    :param root_monkey: (Monkey) root monkey to start the search from
    :return: (bool) boolean indicating whether `humn` has been found
    """
    if root_monkey.name == 'humn':
        return True
    if root_monkey.left_operand and root_monkey.right_operand:
        if root_monkey.left_operand_name == 'humn' or root_monkey.right_operand_name == 'humn':
            return True
        if search_for_monkey(root_monkey.left_operand):
            return True
        return search_for_monkey(root_monkey.right_operand)
    return False


def get_inverse_operator(operator):
    """
    Helper to return the inverse operator.
    :param operator: (str) the operator
    :return: (str) the inverse operator
    """
    if operator == '+':
        return '-'
    if operator == '-':
        return '+'
    if operator == '*':
        return '/'
    return '*'


def evaluate_operation(operator, a, b):
    """
    Helper to evaluate an operation. Could do the same with a look-up table and the package
    `operations`.
    :param operator: (str) the operator
    :param a: (int) first operand
    :param b: (int) second operand
    :return: (int) the result of the operation
    """
    if operator == '+':
        return a + b
    if operator == '-':
        return a - b
    if operator == '*':
        return a * b
    return a / b


def determine_humn_monkey_value(root_monkey, target_value):
    """
    Recursively searches for the humn monkey value based on a target value (value of the monkey's
    parent).
    :param root_monkey: (Monkey) monkey to start the search from
    :param target_value: (int) value the root monkey has to have
    :return: (int) value of the humn monkey
    """
    if root_monkey.name == 'humn':
        return int(target_value)

    # determine to which branch to go
    operator = get_inverse_operator(root_monkey.operator)

    if search_for_monkey(root_monkey.left_operand):
        # left side: just do the inverse operation
        new_target_value = evaluate_operation(operator=operator, a=target_value,
                                              b=root_monkey.right_operand.get_value())
        return determine_humn_monkey_value(root_monkey.left_operand, target_value=new_target_value)

    # else: care for the right side
    if operator in ['-', '/']:
        new_target_value = evaluate_operation(operator=operator, a=target_value,
                                              b=root_monkey.left_operand.get_value())
    else:
        new_target_value = evaluate_operation(operator=root_monkey.operator,
                                              a=root_monkey.left_operand.get_value(),
                                              b=target_value)
    return determine_humn_monkey_value(root_monkey.right_operand, target_value=new_target_value)


class Monkey:
    """
    Class representing a monkey.
    """
    def __init__(self, name, value_or_operator, left_operand_name=None, right_operand_name=None):
        """
        Initializes a monkey class.
        :param name: (str) the name of the monkey
        :param value_or_operator: (str) a value (parsed as int) or an operator
        :param left_operand_name: (str) name of the monkey determining the value on the left side
                                  of the operation, if available
        :param right_operand_name: (str) name of the monkey determining the value on the right side
                                   of the operation, if available
        """
        self.name = name
        self.value = None
        if isinstance(value_or_operator, int):
            self.value = value_or_operator
        else:
            self.operator = value_or_operator

        self.left_operand_name = left_operand_name
        self.right_operand_name = right_operand_name
        self.left_operand = None
        self.right_operand = None

    def set_operators(self, monkey_list):
        """
        Sets the Monkey operators, if needed.
        :param monkey_list: (list) list of all Monkey objects
        :return:
        """
        if self.left_operand_name is not None and self.right_operand_name is not None:
            self.left_operand = monkey_list[self.left_operand_name]
            self.right_operand = monkey_list[self.right_operand_name]

    def get_value(self):
        """
        Helper to (recursively) get the value of a monkey.
        :return: (int) the value of the monkey
        """
        return self.value if self.value is not None else self.get_operation_result()

    def get_operation_result(self):
        """
        If no value is present, determines the value based on the left and right operands, and
        sets the value.
        :return: (int) the value of the monkey
        """
        left_value = self.left_operand.get_value()
        right_value = self.right_operand.get_value()
        self.value = evaluate_operation(operator=self.operator, a=left_value, b=right_value)
        return self.value

    def __repr__(self):
        """
        Helper for debugging.
        :return:
        """
        return self.name


def day21():
    """
    Prints the results for the two day 21 riddles.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 21. Run "
                                                 "`python day21/day21.py` for the first part, "
                                                 "and `python day21/day21.py --part-2` for the "
                                                 "second part.")
    parser.add_argument('--part-2', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        lines = [line.strip() for line in file.readlines()]

    # parse the input to Monkey instances
    monkeys = {}
    for line in lines:
        splitted_line = line.replace(':', '').split(' ')
        monkey_name = splitted_line[0]
        left_operand_name, right_operand_name = None, None
        if len(splitted_line) == 4:
            left_operand_name, value_or_operator, right_operand_name = splitted_line[1:]
        else:
            value_or_operator = int(splitted_line[1])
        monkeys[monkey_name] = Monkey(name=monkey_name, value_or_operator=value_or_operator,
                                      left_operand_name=left_operand_name,
                                      right_operand_name=right_operand_name)

    # set the operators of the monkeys, if necessary
    for monkey_name, monkey in monkeys.items():
        monkey.set_operators(monkey_list=monkeys)

    # calculate the values for all monkeys once
    root_value = monkeys['root'].get_value()

    if not args.part_2:
        print(f"The monkey named `root` yells the following value: {int(root_value)}")

    else:
        # determine starting branches
        if search_for_monkey(monkeys['root'].left_operand):
            target_value = monkeys['root'].right_operand.get_value()
            start_monkey = monkeys['root'].left_operand
        else:
            target_value = monkeys['root'].left_operand.get_value()
            start_monkey = monkeys['root'].right_operand

        # recursively calculate the value for the humn monkey
        humn_value = determine_humn_monkey_value(start_monkey, target_value=target_value)
        print(f"To pass the equality test yell: {humn_value}")


if __name__ == '__main__':
    day21()
