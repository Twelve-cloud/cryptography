#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ds_rsa.py: Digistal signature based on RSA algorithm.
"""


from math import gcd as gcd
from ctypes import c_uint32
from primePy import primes
from egcd import egcd
import random
import sys


PRIMES = [x for x in range(0xFFFFFFF, 0xFFFFFFF + 1000) if primes.check(x)]


def fast_exp(val: int, exp: int, mod: int) -> int:
    """
    fast_exp: calculate exp and mod faster.

    Args:
        val (int): val to exp.
        exp (int): exp.
        mod (int): mod.

    Returns:
        int: calculated number.
    """
    a1 = val
    z1 = exp
    x = 1

    while z1 != 0:
        while z1 % 2 == 0:
            z1 = z1 // 2
            a1 = a1 * a1 % mod
        z1 = z1 - 1
        x = x * a1 % mod

    fast_exp = x

    return fast_exp


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


def encrypt(mhash: int, secret_key: dict[str, int]) -> int:
    """
    encrypt: encrypt hash of the message and create signature.

    Args:
        mhash (int): hash of the message.
        secret_key (dict[str, int]): secret key.

    Returns:
        int: signature.
    """
    signature = fast_exp(mhash, secret_key['d'], secret_key['r'])
    return signature


def decrypt(signature: int, public_key: dict[str, int]) -> int:
    """
    decrypt: decrypt signature and return hash of the message.

    Args:
        signature (int): signature.
        public_key (dict[str, int]): public key.

    Returns:
        int: hash of the message.
    """
    mhash = fast_exp(signature, public_key['e'], public_key['r'])
    return mhash


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


def sign_message(message: str, secret_key: dict[str, int]) -> tuple[str, int]:
    """
    sign_message: sign message.

    Args:
        message (str): source message.
        secret_key (dict[str, int]): secret key.

    Returns:
        tuple[str, int]: message and signature.
    """
    mhash = FNV1AHash(message)
    signature = encrypt(mhash, secret_key)
    return message, signature


def check_message_signature(message: str, signature: int, public_key: dict[str, int]) -> bool:
    """
    check_message_signature: check signature of the message.

    Args:
        message (str): source message.
        signature (int): signature.
        public_key (dict[str, int]): public key.

    Returns:
        bool: True or False.
    """
    mhash = FNV1AHash(message)
    shash = decrypt(signature, public_key)
    return mhash == shash


def sign_file(filename: str, secret_key: dict[str, int]) -> None:
    """
    sign_file: sign file.

    Args:
        filename (str): filename of the file.
        secret_key (dict[str, int]): secret key.
    """
    with open(filename) as file:
        message, signature = sign_message(file.read(), secret_key)
        sfilename = input('Destination filename: ')

        with open(sfilename, 'w') as sfile:
            sfile.write(f'{message}\n{signature}')


def check_file_signature(filename: str, public_key: dict[str, int]) -> None:
    """
    check_file_signature: check signature of the file.

    Args:
        filename (str): filename of the file.
        public_key (dict[str, int]): public key.
    """
    with open(filename) as file:
        lines = file.readlines()
        signature = int(lines[-1])
        result = check_message_signature(''.join(lines[:-2]), signature, public_key)
        sys.stdout.write(f'{result}\n')


if __name__ == '__main__':
    assert sys.argv[1] and sys.argv[2]

    if sys.argv[1] == '-g' and sys.argv[2] == 'keys':
        public_key, secret_key = generate_keys()
        sys.stdout.write(f'pub: {public_key}\nsec: {secret_key}\n')
    elif sys.argv[1] == '-s':
        assert sys.argv[3]
        sign_file(sys.argv[2], eval(sys.argv[3]))
    elif sys.argv[1] == '-c':
        assert sys.argv[3]
        check_file_signature(sys.argv[2], eval(sys.argv[3]))
