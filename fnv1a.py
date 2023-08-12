#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fnv1a.py: FNV1A digest algorithm.
"""


from ctypes import c_uint32
import sys


def FNV1AHash(text: str) -> int:
    """
    FNV1AHash: calculate hash according to FNV1A algorithm.

    Args:
        text (str): source text.

    Returns:
        int: hash digest.
    """
    FNV_prime = 0x1000193
    FNV_offset_basic = 0x811C9DC5

    digest = FNV_offset_basic

    for item in text:
        byte_of_data = ord(item)
        digest = c_uint32(digest ^ byte_of_data).value
        digest = c_uint32(digest * FNV_prime).value

    return digest


if __name__ == '__main__':
    assert sys.argv[1]

    if len(sys.argv) == 3:
        if sys.argv[2] == '-hex':
            sys.stdout.write(f'{hex(FNV1AHash(sys.argv[1]))}\n')
        elif sys.argv[2] == '-bin':
            sys.stdout.write(f'{bin(FNV1AHash(sys.argv[1]))}\n')
        elif sys.argv[2] == '-oct':
            sys.stdout.write(f'{oct(FNV1AHash(sys.argv[1]))}\n')
    else:
        sys.stdout.write(f'{FNV1AHash(sys.argv[1])}\n')
