"""
Advent of code - day 9
(c) Wout Boerdijk
"""

from pathlib import Path
import argparse
import numpy as np
import cv2


class Knot:
    """
    Class representing a knot.
    """
    def __init__(self, parent=None, child=None):
        """
        Initializes a knot.
        :param parent: (Knot) optional parent knot
        :param child: (Knot) optional child knot
        """
        self.parent = parent
        self.child = child
        self.x_pos = 0
        self.y_pos = 0
        self.prev_positions = [(self.x_pos, self.y_pos)]

    def move(self, direction=None):
        """
        Moves into a certain direction. Also updates all children.
        :param direction:
        :return:
        """
        if direction == 'L':
            self.x_pos -= 1
        elif direction == 'R':
            self.x_pos += 1
        elif direction == 'U':
            self.y_pos += 1
        elif direction == 'D':
            self.y_pos -= 1
        else:
            parent_x_offset = self.parent.x_pos - self.x_pos
            parent_y_offset = self.parent.y_pos - self.y_pos
            if not (abs(parent_x_offset) <= 1 and abs(parent_y_offset) <= 1):
                valid_spots_parent_view = get_connection_kernel(connectivity='4',
                                                                x_offset=parent_x_offset,
                                                                y_offset=parent_y_offset)
                valid_spots_know_view = get_connection_kernel(connectivity='8')
                intersection = valid_spots_parent_view.intersection(valid_spots_know_view)
                if len(intersection) == 0:  # happens if the snake moves diagonally
                    valid_spots_parent_view = get_connection_kernel(connectivity='8',
                                                                    x_offset=parent_x_offset,
                                                                    y_offset=parent_y_offset)
                    intersection = valid_spots_parent_view.intersection(valid_spots_know_view)
                assert len(intersection) == 1
                x_pos, y_pos = list(intersection)[0]
                self.x_pos += x_pos
                self.y_pos += y_pos
        self.prev_positions.append((self.x_pos, self.y_pos))

        if self.child is not None:
            self.child.move(direction=None)

    def get_tail(self):
        """
        Returns the tail of a set of knots.
        :return: (Knot) the tail
        """
        if self.child is not None:
            return self.child.get_tail()
        return self

    def get_prev_positions_recursively(self):
        """
        Returns all previous positions, including all positions of the child(ren).
        :return: (list) list of lists
        """
        all_prev_positions = [self.prev_positions]
        if self.child is not None:
            all_prev_positions += self.child.get_prev_positions_recursively()
        return all_prev_positions


def get_connection_kernel(connectivity='4', x_offset=0, y_offset=0):
    """
    Returns a kernel representation, intended for matching for position retrieval.
    :param connectivity: (str) 4-, 8- or 25- connectivity grid.
    :param x_offset: (int) x offset applied to the kernel
    :param y_offset: (int) y offset applied to the kernel
    :return: (set) connectivity kernel
    """
    if connectivity == '4':
        arr = np.array([0, 0, -1, 1])
        stack = np.stack((arr + x_offset, arr[::-1] + y_offset), axis=1)
        return {(stack_x, stack_y) for (stack_x, stack_y) in stack}
    if connectivity == '8':
        arr = np.array([-1, 0, 1]).repeat(3, axis=0).reshape(3, 3)
        stack = np.stack((arr + x_offset, arr.T + y_offset), axis=-1).reshape(-1, 2)
        return {(stack_x, stack_y) for (stack_x, stack_y) in stack}
    raise NotImplementedError


def plot_knot(all_knot_indices):
    """
    Iteratively plots all knots.
    :param all_knot_indices: (list) list of lists representing all knot indices
    :return:
    """
    # shift indices to positive range first
    head_indices = np.array(all_knot_indices[0])
    tail_indices = np.array(all_knot_indices[0])

    min_x, min_y = np.abs(head_indices.min(axis=0))
    head_indices[:, 0] += min_x
    head_indices[:, 1] += min_y
    tail_indices[:, 0] += min_x
    tail_indices[:, 1] += min_y

    width, height = head_indices.max(axis=0) + 1

    colors = 1 / np.arange(1, len(all_knot_indices) + 1)

    for num_steps in range(len(all_knot_indices[0])):
        plot = np.zeros((height * 5, width * 5))
        for num_knot in enumerate(all_knot_indices):
            x_pos, y_pos = all_knot_indices[num_knot][num_steps]
            plot[5*y_pos:5*y_pos+5, 5*x_pos:5*x_pos+5] = colors[num_knot]
        cv2.imshow('arr', np.flipud(plot))
        cv2.waitKey(0)


def day9():
    """
    Prints the results for the two day 9 riddles.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 9. Run "
                                                 "`python day9/day9.py` for the first part, "
                                                 "and `python day9/day9.py --part-2` for the "
                                                 "second part. Add `--viz` for an interactive "
                                                 "visualization.")
    parser.add_argument('--part-2', default=False, action='store_true')
    parser.add_argument('--viz', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        movements = [line.strip().split(' ') for line in file.readlines()]

    movements = [(direction, int(num_steps)) for direction, num_steps in movements]

    head = Knot()
    num_childs = 9 if args.part_2 else 1
    current_knot = head
    for _ in range(num_childs):
        current_knot.child = Knot(parent=current_knot)
        current_knot = current_knot.child

    for direction, num_steps in movements:
        for _ in range(num_steps):
            head.move(direction=direction)

    if args.viz:
        plot_knot(head.get_prev_positions_recursively())

    print(f"Number of unique positions: {len(set(head.get_tail().prev_positions[1:]))}")


if __name__ == '__main__':
    day9()
