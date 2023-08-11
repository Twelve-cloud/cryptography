#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
seds.py: S-DES algorithm.
"""


from typing import TypeVar
from math import ceil
import sys


KEY = 666
P10 = (3, 5, 2, 7, 4, 10, 1, 9, 8, 6)
P8 = (6, 3, 7, 4, 8, 5, 10, 9)
P4 = (2, 4, 3, 1)
EP = (4, 1, 2, 3, 2, 3, 4, 1)
IP1 = (2, 6, 3, 1, 4, 8, 5, 7)
IP2 = (4, 1, 3, 5, 7, 2, 8, 6)
S1 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S2 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]


T = TypeVar('T')
Mx = list[list[T]]


def transform_to_bits(number: int, bitq: int = None) -> list[int]:
    """
    transform_to_bits: transform number to list of bits.

    Args:
        number (int): source number.
        bitq (int, optional): if not None then bin number shoud be
                              increased to size bitq otherwise should not.

    Returns:
        list[int]: list of bits.
    """
    bits = [int(x) for x in f'{number:b}']

    if bitq is None:
        return bits

    while len(bits) < bitq:
        bits.insert(0, 0)

    return bits


def permutate_according_to_rule(bits: list[int], rule: tuple[int, ...]) -> list[int]:
    """
    permutate_according_to_rule: permutate list of bits according to the rule.

    Args:
        bits (list[int]): list of bits.
        rule (tuple[int, ...]): permutation rule.

    Returns:
        list[int]: permutated list of bits.
    """
    permutated_bits = [bits[i - 1] for i in rule]
    return permutated_bits


def split_by(bits: list[int], one_part_quantity: int) -> list[int]:
    """
    split_by: split list of bits by several parts where one part size is one_part_quanity.

    Args:
        bits (list[int]): list of bits.
        one_part_quantity (int): size of one part.

    Returns:
        list[int]: list with parts where each part is a list of bits.
    """
    splitted = [[] for x in range(ceil(len(bits) / one_part_quantity))]

    current, i = 0, 0
    while bits:
        if i == one_part_quantity:
            current += 1
            i = 0
        splitted[current].append(bits.pop(0))
        i += 1

    return splitted


def shift_bits_to(bits: list[int], direction: str, quantity: int) -> list[int]:
    """
    shift_bits_to: shift bits sequence in direction to quantity.

    Args:
        bits (list[int]): list of bits.
        direction (str): shift direction.
        quantity (int): offset to shift.

    Returns:
        list[int]: shifted list of bits.
    """
    assert direction == 'l' or direction == 'r'

    if direction == 'l':
        return bits[quantity:] + bits[:quantity]
    else:
        return bits[len(bits) - quantity:] + bits[:quantity + 1]


def generate_keys(KEY: int) -> tuple[list[int], list[int]]:
    """
    generate_keys: generate two 8-bit keys based on 10-bit KEY.

    Args:
        KEY (int): any number which you want to be a KEY.

    Returns:
        tuple[list[int], list[int]]: tuple of 2 8-bit keys.
    """
    KEY = transform_to_bits(KEY, 10)
    permutated_bits = permutate_according_to_rule(KEY, P10)

    lpart, rpart = split_by(permutated_bits, 5)

    lpart = shift_bits_to(lpart, 'l', 1)
    rpart = shift_bits_to(rpart, 'l', 1)

    K1 = permutate_according_to_rule(lpart + rpart, P8)

    lpart = shift_bits_to(lpart, 'l', 2)
    rpart = shift_bits_to(rpart, 'l', 2)

    K2 = permutate_according_to_rule(lpart + rpart, P8)

    return K1, K2


def box_processing(left: list[int], right: list[int], S1: Mx[int], S2: Mx[int]) -> list[int]:
    """
    box_processing: special processing of bits.

    Args:
        left (list[int]): list part of bits.
        right (list[int]): right part of bits.
        S1 (Mx[int]): S1 box.
        S2 (Mx[int]): S2 box.

    Returns:
        list[int]: pocessed list of bits.
    """
    left_number = S1[int(f'{left[0]}{left[-1]}', base=2)][int(f'{left[1]}{left[2]}', base=2)]
    right_number = S2[int(f'{right[0]}{right[-1]}', base=2)][int(f'{right[1]}{right[2]}', base=2)]

    left_bits = transform_to_bits(left_number, 2)
    right_bits = transform_to_bits(right_number, 2)

    return left_bits + right_bits


def round_(bits: list[int], key: list[int]) -> list[int]:
    """
    round_: perform round of S-DES algorithm.

    Args:
        bits (list[int]): list of bits.
        key (list[int]): 8-bit key.

    Returns:
        list[int]: rounded list of bits.
    """
    lpart, rpart = split_by(bits, 4)

    extented_rpart = permutate_according_to_rule(rpart, EP)
    xor_rpart = [x ^ y for x, y in zip(extented_rpart, key)]
    xor_l, xor_r = split_by(xor_rpart, 4)

    box_bits = box_processing(xor_l, xor_r, S1, S2)
    box_permutated = permutate_according_to_rule(box_bits, P4)

    xor_bits = [x ^ y for x, y in zip(lpart, box_permutated)]
    bits = xor_bits + rpart

    return bits


def encrypt(symbol: str, K1: list[int], K2: list[int]) -> str:
    """
    encrypt: encrypt one symbol.

    Args:
        symbol (str): symbol to encode.
        K1 (list[int]): first 8-bit key.
        K2 (list[int]): second 8-bit key.

    Returns:
        str: encoded symbol.
    """
    symbol_code = ord(symbol)
    bits = transform_to_bits(symbol_code, 8)

    permutated_bits = permutate_according_to_rule(bits, IP1)

    round_bits = round_(permutated_bits, K1)

    lpart, rpart = split_by(round_bits, 4)
    round_bits = rpart + lpart

    round_bits = round_(round_bits, K2)

    permutated_bits = permutate_according_to_rule(round_bits, IP2)
    permutated_bits = [str(x) for x in permutated_bits]

    encoded_symbol_code = int(''.join(permutated_bits), base=2)
    encoded_symbol = chr(encoded_symbol_code)

    return encoded_symbol


def decrypt(symbol: str, K1: list[int], K2: list[int]) -> list[int]:
    """
    decrypt: decrypt one symbol.

    Args:
        symbol (str): symbol to decode.
        K1 (list[int]): first 8-bit key.
        K2 (list[int]): second 8-bit key.

    Returns:
        str: decoded symbol.
    """
    symbol_code = ord(symbol)
    bits = transform_to_bits(symbol_code, 8)

    permutated_bits = permutate_according_to_rule(bits, IP1)

    round_bits = round_(permutated_bits, K2)

    lpart, rpart = split_by(round_bits, 4)
    round_bits = rpart + lpart

    round_bits = round_(round_bits, K1)

    permutated_bits = permutate_according_to_rule(round_bits, IP2)
    permutated_bits = [str(x) for x in permutated_bits]

    decoded_symbol_code = int(''.join(permutated_bits), base=2)
    decoded_symbol = chr(decoded_symbol_code)

    return decoded_symbol


def encrypt_file(filename: str) -> None:
    """
    encrypt_file: encrypt file with name filename.

    Args:
        filename (str): filename of source file.
    """
    K1, K2 = generate_keys(KEY)

    with open(filename) as file:
        encoded_text = ''.join([encrypt(x, K1, K2) for x in file.read()])

        efilename = input('Destination filename: ')

        with open(efilename, 'w') as efile:
            efile.write(encoded_text)


def decrypt_file(filename: str) -> None:
    """
    decrypt_file: decrypt file with name filename.

    Args:
        filename (str): filename of source file.
    """
    K1, K2 = generate_keys(KEY)

    with open(filename) as file:
        decoded_text = ''.join([decrypt(x, K1, K2) for x in file.read()])

        dfilename = input('Destination filename: ')

        with open(dfilename, 'w') as efile:
            efile.write(decoded_text)


if __name__ == '__main__':
    assert sys.argv[1] and sys.argv[2]

    if sys.argv[1] == '-e':
        encrypt_file(sys.argv[2])
    else:
        decrypt_file(sys.argv[2])
