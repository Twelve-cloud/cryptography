#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seds.py: S-DES algorithm.
"""


from math import ceil


KEY = 666
P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8 = (6, 3, 7, 4, 8, 5, 10, 9)


def transform_to_bits(number, bitq=None):
    bits = list(f'{number:b}')

    if bitq is None:
        return bits

    while len(bits) < bitq:
        bits.insert(0, 0)

    return bits


def permutate_according_to_rule(bits, rule):
    assert len(bits) >= len(rule)
    permutated_bits = [bits[i - 1] for i in rule]
    return permutated_bits


def split_by(bits, one_part_quantity):
    splitted = [[] for x in range(ceil(len(bits) / one_part_quantity))]

    current, i = 0, 0
    while bits:
        if i == one_part_quantity:
            current += 1
            i = 0
        splitted[current].append(bits.pop(0))
        i += 1

    return splitted


def shift_bits_to(bits, direction, quantity):
    assert direction == 'l' or direction == 'r'

    if direction == 'l':
        return bits[quantity:] + bits[:quantity]
    else:
        return bits[len(bits) - quantity:] + bits[:quantity + 1]


def generate_keys(KEY):
    KEY = transform_to_bits(KEY, 10)
    permutated_bits = permutate_according_to_rule([1, 0, 0, 1, 0, 1, 0, 0, 1, 1], P10)

    lpart, rpart = split_by(permutated_bits, 5)

    lpart = shift_bits_to(lpart, 'l', 1)
    rpart = shift_bits_to(rpart, 'l', 1)

    K1 = permutate_according_to_rule(lpart + rpart, P8)

    lpart = shift_bits_to(lpart, 'l', 2)
    rpart = shift_bits_to(rpart, 'l', 2)

    K2 = permutate_according_to_rule(lpart + rpart, P8)

    return K1, K2


if __name__ == '__main__':
    K1, K2 = generate_keys(KEY)
    print(K1, K2)
