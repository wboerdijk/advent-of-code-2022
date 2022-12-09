"""
Advent of code - day 7
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path


def get_size_of_dirs(directory):
    """
    Returns the size of all dirs below the given dir.
    :param directory: (Dir) a directory
    :return: (list) list of ints representing the sizes
    """
    dir_sizes = []
    for sub_dir in directory.dirs.values():
        dir_sizes.append(sub_dir.calculate_size())
        dir_sizes.extend(get_size_of_dirs(sub_dir))
    return dir_sizes


class Directory:
    """
    Class representing a directory.
    """
    def __init__(self, parent=None):
        """
        Initializes a directory.
        :param parent: (Directory) Pointer to a parent directory, if not the root.
        """
        self.parent = parent
        self.dirs = {}
        self.files = {}
        self.size = 0

    def calculate_size(self):
        """
        Recursively calculates the size for all sub-(sub-...)directories, if existing.
        Sets `self.size`.
        :return: (int) total size of the directory including all sub-(sub-...)directories and files.
        """
        dir_sizes = sum(size for size in [child_dir.calculate_size() for child_dir in
                                          self.dirs.values()]
                        if size is not None)
        self.size = sum(self.files.values()) + dir_sizes
        return self.size

    def get_root(self):
        """
        Returns the up-most directory root.
        :return: (Dir) the directory's root.
        """
        if self.parent:
            return self.parent.get_root()
        return self


def day7():
    """
    Prints the results for the two day 7 riddles.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 7. Run "
                                                 "`python day7/day7.py` for the first part, "
                                                 "and `python day7/day7.py --part-2` for the "
                                                 "second part.")
    parser.add_argument('--part-2', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        data_lines = [data_line.strip() for data_line in file.readlines()]

    # first line starts with `cd /`, then follows an `ls`
    # we assume no other `cd /`
    # every following line can be put into a dict
    curr_dir = Directory(parent=None)
    for data_line in data_lines[2:]:
        if data_line.startswith('$'):  # don't need to check the other condition
            if data_line[2:4] == 'cd':
                key = data_line.split(' ')[-1]
                if key == '..':
                    curr_dir = curr_dir.parent
                else:
                    assert key in curr_dir.dirs
                    curr_dir = curr_dir.dirs[key]
        else:  # lists a directory or a file
            dir_or_size, name = data_line.split(' ')
            if dir_or_size == 'dir':
                curr_dir.dirs[name] = Directory(parent=curr_dir)
            else:
                curr_dir.files[name] = int(dir_or_size)

    # go back to the parent, and recursively calculate the size for all directories
    parent = curr_dir.get_root()
    total_size = parent.calculate_size()

    # get the size of all dirs
    dir_sizes = get_size_of_dirs(parent)

    if args.part_2:
        # select the one freeing up as much space as possible
        # assumes all dirs have a different size
        min_space_to_delete = 30000000 - (70000000 - total_size)
        dirs_above_min_space_required = sorted([dir_size for dir_size in dir_sizes
                                                if dir_size >= min_space_to_delete])
        print(f"Size of dir to delete: {dirs_above_min_space_required[0]}")

    else:
        print(f"Total size (<100000): {sum(s for s in dir_sizes if s < 100000)}")


if __name__ == '__main__':
    day7()
