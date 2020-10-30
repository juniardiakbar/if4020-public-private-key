import random

from os import path
from src.helper.math import modular_pow

PRIME_LIST_FILE_NAME = path.abspath(path.join(path.dirname(__file__), 'primes-300k-to-400k.txt'))
BLOCK_SIZE = 2

def generate_pair(public_key_path, private_key_path):
    prime_list = open(PRIME_LIST_FILE_NAME).read().splitlines()
    p = int(random.choice(prime_list))
    g = random.randint(2, p - 1)
    x = random.randint(1, p - 2)
    y = modular_pow(g, x, p)

    public_key = (y, g, p)
    private_key = (x, p)

    public_key_str = ', '.join([str(x) for x in public_key])
    private_key_str = ', '.join([str(x) for x in private_key])

    f_public = open(public_key_path, 'w')
    f_public.write(public_key_str)
    f_public.close()

    f_private = open(private_key_path, 'w')
    f_private.write(private_key_str)
    f_private.close()

    return public_key, private_key

def encrypt(message, public_key):
    y, g, p = [int(x) for x in public_key.split(', ')]
    blocks = []
    block = ord(message[0]) if len(message) > 0 else -1

    if len(message) % BLOCK_SIZE:
        message += chr(0)
    for i in range(1, len(message)):
        if (i % BLOCK_SIZE == 0):
            blocks.append(block)
            block = 0
        block = block * 1000 + ord(message[i])
    blocks.append(block)

    k = random.randint(1, p - 2)
    for i in range(len(blocks)):
        a = modular_pow(g, k, p)
        b = (modular_pow(y, k, p) * blocks[i]) % p
        blocks[i] = (a, b)

    flattened = [str(item) for pair in blocks for item in pair]
    stringified = ' '.join(flattened)
    return stringified

def decrypt(stringified, private_key):
    print(private_key)
    x, p = [int(x) for x in private_key.split(', ')]

    split = stringified.split(' ')
    blocks = []

    for i in range(0, len(split), 2):
        a = int(split[i])
        b = int(split[i + 1])
        blocks.append((a, b))

    message = ''
    for a, b in blocks:
        a_x_inverse = modular_pow(a, p - 1 - x, p)
        plain = (b * a_x_inverse) % p

        tmp = ''
        for _ in range(BLOCK_SIZE):
            tmp = chr(plain % 1000) + tmp
            plain //= 1000
        message += tmp
    return message
