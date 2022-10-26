#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
caesar: caesar algorithm. Formula:
    1) Ek(i) = (i+k) mod 26.
    2) Dk(i) = (i+26-k) mod 26.
"""


def caesar_upper_encryption(text: str, key: int = 3) -> str:
    """
    caesar_upper_encryption: caesar encryption algorithm for english
    alphabet in uppercase.
    """
    return ''.join([chr(((ord(x) - 65 + key) % 26) + 65) for x in text])


def caesar_upper_decryption(text: str, key: int = 3) -> str:
    """
    caesar_upper_decryption: caesar decryption algorithm for english
    alphabet in uppercase.
    """
    return ''.join([chr(((ord(x) - 65 + 26 - key) % 26) + 65) for x in text])


def caesar_lower_encryption(text: str, key: int = 3) -> str:
    """
    caesar_lower_encryption: caesar encryption algorithm for english
    alphabet in lowercase.
    """
    return ''.join([chr(((ord(x) - 97 + key) % 26) + 97) for x in text])


def caesar_lower_decryption(text: str, key: int = 3) -> str:
    """
    caesar_lower_decryption: caesar decryption algorithm for english
    alphabet in lowercase.
    """
    return ''.join([chr(((ord(x) - 97 + 26 - key) % 26) + 97) for x in text])


def caesar_encryption(text: str, key: int = 3) -> str:
    """
    caesar_encryption: caesar encryption algorithm for english
    alphabet in any register.
    """
    return ''.join([chr(((ord(x) - (65 if x.isupper() else 97) + key) % 26) + (65 if x.isupper() else 97)) for x in text])


def caesar_decryption(text: str, key: int = 3) -> str:
    """
    caesar_decryption: caesar decryption algorithm for english
    alphabet in any register.
    """
    return ''.join([chr(((ord(x) - (65 if x.isupper() else 97) + 26 - key) % 26) + (65 if x.isupper() else 97)) for x in text])


def caesar_ascii_encryption(text: str, key: int = 3) -> str:
    """
     caesar_ascii_encryption: caesar encryption algorithm for ascii symbols.
    """
    return ''.join([chr((ord(x) + key) % 256) for x in text])


def caesar_ascii_decryption(text: str, key: int = 3) -> str:
    """
    caesar_ascii_decryption: caesar decryption algorithm for ascii symbols.
    """
    return ''.join([chr((ord(x) + 256 - key) % 256) for x in text])


if __name__ == '__main__':
    assert caesar_upper_encryption('CRYPTOGRAPHY') == 'FUBSWRJUDSKB'
    assert caesar_upper_decryption('FUBSWRJUDSKB') == 'CRYPTOGRAPHY'

    assert caesar_lower_encryption('cryptography') == 'fubswrjudskb'
    assert caesar_lower_decryption('fubswrjudskb') == 'cryptography'

    assert caesar_encryption('cryPTOgraphy') == 'fubSWRjudskb'
    assert caesar_decryption('fubSWRjudskb') == 'cryPTOgraphy'

    assert caesar_ascii_encryption('cryPTOgraphy') == 'fu|SWRjudsk|'
    assert caesar_ascii_decryption('fu|SWRjudsk|') == 'cryPTOgraphy'
