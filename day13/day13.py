"""
Advent of code - day 13
(c) Wout Boerdijk
"""

import argparse
from pathlib import Path


def to_list(item):
    """
    Helper to convert an int to a list.
    :param item: (any) the item to convert to a list, if it's an int
    :return: (any) list if the item is an int, else the item
    """
    if isinstance(item, int):
        return [item]
    return item


def compare_pairs(pair_a, pair_b):
    """
    Recursively compares a packet pair according to the rules.
    :param pair_a: (list, int) a list or int
    :param pair_b: (list, int) a list or int
    :return: (str) one of 'smaller', 'equal', 'larger'
    """
    if isinstance(pair_a, int) and isinstance(pair_b, int):
        if pair_a == pair_b:
            return 'equal'
        if pair_a < pair_b:
            return 'smaller'
        return 'larger'

    pair_a = to_list(pair_a)
    pair_b = to_list(pair_b)

    index = 0
    for index, (item_a, item_b) in enumerate(zip(pair_a, pair_b)):
        comparison = compare_pairs(item_a, item_b)
        if comparison in ['smaller', 'larger']:
            return comparison

    # evaluate length
    if len(pair_a[index:]) != len(pair_b[index:]):
        if len(pair_a[index:]) < len(pair_b[index:]):
            return 'smaller'
        return 'larger'
    return 'equal'


def sort_packets(packets):
    """
    Performs standard line sorting.
    :param packets: (list) list of packets
    :return: (list) sorted list of packets
    """
    sorted_packets = []
    while len(packets) != 0:
        # search for smallest packet
        smallest_packet = 0
        for index in range(1, len(packets)):
            is_smaller = compare_pairs(packets[smallest_packet], packets[index])
            if is_smaller == 'larger':
                smallest_packet = index
        sorted_packets.append(packets.pop(smallest_packet))
    return sorted_packets


def insert_packet_to_packets(packet, packets):
    """
    Inserts a packet to a (sorted) list of packets.
    :param packet: (list) list of ints
    :param packets: (list) list of packets
    :return: (list, int) tuple of updated list of packets, and the insertion index + 1
    """
    for index in range(len(packets)):
        if compare_pairs(packet, packets[index]) == 'smaller':
            return packets[:index] + [packet] + packets[index:], index + 1
    return packets, -1


def day13():
    """
    Prints the results for the two day 13 riddles.
    :return:
    """
    parser = argparse.ArgumentParser(description="Advent of code - day 13. Run "
                                                 "`python day13/day13.py` for the first part, "
                                                 "and `python day13/day13.py --part-2` for the "
                                                 "second part.")
    parser.add_argument('--part-2', default=False, action='store_true')
    args = parser.parse_args()

    with open(Path(__file__).parent.resolve().joinpath('input.txt'), 'r', encoding='utf-8') as file:
        packets = [packet.strip() for packet in file.readlines()]

    packets = [packet for packet in packets if packet != '']

    # parse packets to lists
    if args.part_2:
        packet_sets = [[eval(packet) for packet in packets]]
    else:
        packet_sets = []
        for num_packet in range(0, len(packets), 2):
            packet_sets.append([eval(packets[num_packet]), eval(packets[num_packet + 1])])

    correctly_ordered_pairs = 0
    for i, packet_set in enumerate(packet_sets):
        sorted_packets = sort_packets(packet_set[:])
        if sorted_packets == packet_set:
            correctly_ordered_pairs += i+1

    if args.part_2:
        sorted_packets_with_start_packet, start_divider_packet_index = insert_packet_to_packets(
            packet=[[2]], packets=sorted_packets)
        _, end_divider_packet_index = insert_packet_to_packets(packet=[[6]],
                                                           packets=sorted_packets_with_start_packet)
        print(f"Multiplication of divider packet indices: "
              f"{start_divider_packet_index * end_divider_packet_index}")
    else:
        print(f"Multiplication of correctly ordered pair indices: {correctly_ordered_pairs}")


if __name__ == '__main__':
    day13()
