#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lsb.py: Least significant bit algorithm.
"""


import sys


def write_hidden_message(filename: str, message: str, bits: int = 1) -> int:
    """
    write_hidden_message: write hidden message in the image.

    Args:
        filename (str): filename of the file.
        message (str): source message.
        bits (int, optional): how much bits will be changed. Defaults to 1.

    Returns:
        int: length of the message.
    """
    with open(filename, 'rb') as file:
        pixels = bytearray(file.read())
        mid = len(pixels) // 2
        msg_bits = ''.join([f'{ord(x):08b}' for x in message])
        msg_len_bits = len(msg_bits)

        while msg_bits:
            byte = pixels[mid]
            bits_of_byte = f'{byte:b}'
            bits_of_byte = bits_of_byte[:-bits] + msg_bits[:bits]
            byte = int(bits_of_byte, base=2)
            pixels[mid] = byte
            msg_bits = msg_bits[bits:]
            mid += 1

        dfilename = input('Destination filename: ')

        with open(dfilename, 'wb') as wfile:
            wfile.write(pixels)

        return msg_len_bits


def read_hidden_message(filename: str, msg_len_bits: int, bits: int = 1) -> str:
    """
    read_hidden_message: read hidden message from the image.

    Args:
        filename (str): filename of the file.
        msg_len_bits (int): length of the hidden message.
        bits (int, optional): how much bits will be changed. Defaults to 1.

    Returns:
        str: hidden message.
    """
    with open(filename, 'rb') as file:
        pixels = file.read()
        mid = len(pixels) // 2

        i, result = 0, ''
        while i < msg_len_bits:
            byte = pixels[mid]
            bits_of_byte = f'{byte:b}'
            result += bits_of_byte[-1]
            i += 1
            mid += 1

        L = []
        while result:
            L.append(chr(int(result[:8], base=2)))
            result = result[8:]

        return ''.join(L)


if __name__ == '__main__':
    assert sys.argv[1] and sys.argv[2] and sys.argv[3]

    if sys.argv[1] == '-w':
        msg_len_bits = write_hidden_message(sys.argv[2], sys.argv[3])
        sys.stdout.write(f'{msg_len_bits}\n')
    elif sys.argv[1] == '-r':
        hidden_message = read_hidden_message(sys.argv[2], int(sys.argv[3]))
        sys.stdout.write(f'{hidden_message}\n')
