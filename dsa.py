#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dsa.py: Digistal signature with DSA algorithm.
"""


from primePy import primes
import hashlib
import random
import sys


PRIMES_Q = [x for x in range(100, 999) if primes.check(x)]
PRIMES_P = [x for x in range(1000, 99999) if primes.check(x)]


def choose_p(primes: list[int]) -> int:
    """
    choose_p: choose p from primes.

    Args:
        primes (list[int]): list of primes.

    Returns:
        int: chosen p.
    """
    P = random.choice(primes)

    while (P - 1) % Q != 0:
        P = random.choice(primes)

    return P


def choose_g(number: range) -> int:
    """
    choose_g: choose g.

    Args:
        number (list[int]): list of ints.

    Returns:
        int: chosen g.
    """
    h = random.choice(number)
    G = h ** ((P - 1) // Q) % P

    while G <= 1:
        h = random.choice(number)
        G = h ** ((P - 1) // Q) % P

    return G


Q = random.choice(PRIMES_Q)
P = choose_p(PRIMES_P)
G = choose_g(range(2, P - 1))


def generate_keys() -> tuple[int, int]:
    """
    generate_keys: generate secret and public keys.

    Returns:
        tuple[int, int]: secret and public keys.
    """
    secret_key = random.choice(range(1, Q))
    public_key = G ** secret_key % P
    return secret_key, public_key


def sign_message(message: str, secret_key: int) -> tuple[str, int, int]:
    """
    sign_message: sign message with secret key.

    Args:
        message (str): source message.
        secret_key (int): secret key.

    Returns:
        tuple[str, int, int]: source message, r and s.
    """
    mhash = int(hashlib.md5(message.encode('UTF-8')).hexdigest(), base=16)
    k = random.choice(range(1, Q))
    r = (G ** k % P) % Q
    s = k ** (Q - 1 - 1) * (mhash + secret_key * r) % Q

    while s == 0 or r == 0:
        k = random.choice(range(1, Q))
        r = (G ** k % P) % Q
        s = k ** (Q - 1 - 1) * (mhash + secret_key * r) % Q

    return message, r, s


def check_message_signature(message: str, r: int, s: int, public_key: int) -> bool:
    """
    check_message_signature: check signature.

    Args:
        message (str): source message.
        r (int): r.
        s (int): s.
        public_key (int): public key.

    Returns:
        bool: True or False.
    """
    mhash = int(hashlib.md5(message.encode('UTF-8')).hexdigest(), base=16)
    w = s ** (Q - 1 - 1) % Q
    u1 = (mhash * w) % Q
    u2 = (r * w) % Q
    v = ((G ** u1 * public_key ** u2) % P) % Q
    return v == r


def sign_file(filename: str, secret_key: int) -> None:
    """
    sign_file: sign file.

    Args:
        filename (str): filename of the file.
        secret_key (int): secret key.
    """
    with open(filename) as file:
        sfilename = input('Destination filename: ')
        message, r, s = sign_message(file.read(), secret_key)

        with open(sfilename, 'w') as sfile:
            sfile.write(f'{message}\n r={r}\n s={s}\n')


def check_file_signature(filename: str, public_key: int, r: int, s: int) -> None:
    """
    check_file_signature: cehck file signature.

    Args:
        filename (str): filename of the file.
        public_key (int): public key.
        r (int): r.
        s (int): s.
    """
    with open(filename) as file:
        lines = file.readlines()
        r = int(lines[-2].split('=')[-1])
        s = int(lines[-1].split('=')[-1])
        result = check_message_signature(''.join(lines[:-3]), r, s, public_key)
        sys.stdout.write(f'{result}\n')


if __name__ == '__main__':
    assert sys.argv[1]

    if sys.argv[1] == '-g':
        secret_key, public_key = generate_keys()
        sys.stdout.write(f'sec: {secret_key}, pub: {public_key}, q: {Q}, p: {P}, g: {G}\n')
    elif sys.argv[1] == '-s':
        Q, P, G = int(sys.argv[5]), int(sys.argv[7]), int(sys.argv[9])
        sign_file(sys.argv[3], int(sys.argv[2]))
    elif sys.argv[1] == '-c':
        Q, P, G = int(sys.argv[9]), int(sys.argv[11]), int(sys.argv[13])
        check_file_signature(sys.argv[7], int(sys.argv[2]), int(sys.argv[4]), int(sys.argv[6]))
