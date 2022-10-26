#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
caesar: Caesar algorithm. Formula:
    1) Ek(i) = (i+k) mod 26.
    2) Dk(i) = (i+26-k) mod 26.
"""


def caesar_encryption(text: str, key: int = 3) -> str:
    """
    caesar_encryption: caesar encryption algorithm for english alphabet in any register.
    """
    return ''.join([chr(((ord(x) - (65 if x.isupper() else 97) + key) % 26) + (65 if x.isupper() else 97)) for x in text])


def caesar_decryption(text: str, key: int = 3) -> str:
    """
    caesar_decryption: caesar decryption algorithm for english alphabet in any register.
    """
    return ''.join([chr(((ord(x) - (65 if x.isupper() else 97) + 26 - key) % 26) + (65 if x.isupper() else 97)) for x in text])


if __name__ == '__main__':
    assert caesar_encryption('cryPTOgraphy') == 'fubSWRjudskb'
    assert caesar_decryption('fubSWRjudskb') == 'cryPTOgraphy'
