#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
caesar_improved.py: Improved caesar algorithm.
Formulas:
    1) Ek(i) = (i*ke) mod n.
    2) Dk(i) = (i*kd) mod n.

Constraints:
    1) ke & n - relatively prime numbers.
    2) kd & n - relatively prime numbers.
    3) (ke * kd) mod n = 1.
"""


from math import gcd


def generate_keys(n: int = 256) -> tuple:
    """
    generate_keys: Generates keys (ke, kd) for cryptography algorithm.
    """
    for i in range(1, n):
        for j in range(2, n):
            if (i * j) % n == 1 and gcd(i, n) == 1 and gcd(j, n) == 1:
                return i, j


def encrypt(text: str, ke: int, n: int = 256) -> str:
    """
    encrypt: Improved caesar encryption algorithm for ASCII codes.
    """
    return ''.join([chr((ord(x) * ke) % n) for x in text])


def decrypt(text: str, kd: int, n: int = 256) -> str:
    """
    decrypt: Improved caesar decryption algorithm for ASCII codes.
    """
    return ''.join([chr((ord(x) * kd) % n) for x in text])


if __name__ == '__main__':
    ke, kd = generate_keys(256)
    assert encrypt('cryptography', ke) == ')VkP\\M5V#P8k'
    assert decrypt(')VkP\\M5V#P8k', kd) == 'cryptography'
