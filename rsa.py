#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
rsa.py: RSA algorithm.
"""


from math import gcd as gcd
from primePy import primes
from egcd import egcd
import random
import sys


PRIMES = [x for x in range(100, 199) if primes.check(x)]


def choose_random_primes(primes: list[int], epsilon: int = 10) -> tuple[int, int]:
    """
    choose_random_primes: choose two prime numbers.

    Args:
        primes(list[int]): list of primes.
        eplison(int, optional): max difference between two random prime numbers. Defaults to 10.

    Returns:
        tuple[int, int]: two random prime numbers.
    """
    p = random.choice(primes)
    q = random.choice(primes)

    while abs(p - q) >= epsilon or p == q:
        p = random.choice(primes)
        q = random.choice(primes)

    return p, q


def choose_e(primes: list[int], x: int) -> int:
    """
    choose_e: choose e.

    Args:
        primes (list[int]): list of primes.
        x (int): x value.

    Returns:
        int: chosen e.
    """
    e = random.choice(primes)
    while (e >= x) or gcd(e, x) != 1:
        e = random.choice(primes)

    return e


def generate_keys() -> tuple[dict, dict]:
    """
    generate_keys: generate public and secret keys.

    Returns:
        tuple[dict, dict]: pair public key and secret key.
    """
    p, q = choose_random_primes(PRIMES)
    r = p * q

    x = (p - 1) * (q - 1)
    e = choose_e(PRIMES, x)

    d = egcd(x, e)[2]

    if d < 0:
        d += x

    public_key = {'e': e, 'r': r}
    secret_key = {'d': d, 'r': r}

    return public_key, secret_key


def encrypt(text: str, public_key: dict[str, int]) -> str:
    """
    encrypt: encrypt text by public key.

    Args:
        text (str): source text.
        public_key (dict[str, int]): public key.

    Returns:
        str: encrypted key.
    """
    codes = [ord(x) for x in text]
    encoded_codes = [x ** public_key['e'] % public_key['r'] for x in codes]
    encoded_text = ''.join(chr(x) for x in encoded_codes)

    return encoded_text


def decrypt(text: str, secret_key: dict[str, int]) -> str:
    """
    decrypt: decrypt text.

    Args:
        text (str): encrypted text.
        secret_key (dict[str, int]): secret key.

    Returns:
        str: decrypted text.
    """
    codes = [ord(x) for x in text]
    decoded_codes = [x ** secret_key['d'] % secret_key['r'] for x in codes]
    decoded_text = ''.join(chr(x) for x in decoded_codes)

    return decoded_text


def encrypt_file(filename: str, public_key: dict[str, int]) -> None:
    """
    encrypt_file: encrypt file.

    Args:
        filename (str): filename of source file.
        public_key (dict[str, int]): public key.
    """
    with open(filename) as file:
        encoded_text = encrypt(file.read(), public_key)

        efilename = input('Destination filename: ')

        with open(efilename, 'w') as efile:
            efile.write(encoded_text)


def decrypt_file(filename: str, secret_key: dict[str, int]) -> None:
    """
    decrypt_file: decrypt file.

    Args:
        filename (str): filename of source file.
        secret_key (dict[str, int]): secret key.
    """
    with open(filename) as file:
        decoded_text = decrypt(file.read(), secret_key)
        dfilename = input('Destination filename: ')

        with open(dfilename, 'w') as dfile:
            dfile.write(decoded_text)


if __name__ == '__main__':
    assert sys.argv[1] and sys.argv[2]

    if sys.argv[1] == '-e':
        assert sys.argv[3]
        encrypt_file(sys.argv[2], eval(sys.argv[3]))
    elif sys.argv[1] == '-d':
        assert sys.argv[3]
        decrypt_file(sys.argv[2], eval(sys.argv[3]))
    elif sys.argv[1] == '-g' and sys.argv[2] == 'keys':
        public_key, secret_key = generate_keys()
        sys.stdout.write(f'pub: {public_key}\nsec: {secret_key}\n')
