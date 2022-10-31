#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
caesar.py: Caesar algorithm.
Formulas:
    1) Ek(i) = (i+k) mod n.
    2) Dk(i) = (i+n-k) mod n.
"""


def encrypt(text: str, k: int = 3, n: int = 256) -> str:
    """
    encrypt: Caesar encryption algorithm for ASCII codes.
    """
    return ''.join([chr((ord(x) + k) % n) for x in text])


def decrypt(text: str, k: int = 3, n: int = 256) -> str:
    """
    decrypt: Caesar decryption algorithm for ASCII codes.
    """
    return ''.join([chr((ord(x) + n - k) % n) for x in text])


if __name__ == '__main__':
    assert encrypt('cryptography') == 'fu|swrjudsk|'
    assert decrypt('fu|swrjudsk|') == 'cryptography'
