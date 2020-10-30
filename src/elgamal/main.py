import random

from os import path
from helper import modular_pow

PRIME_LIST_FILE_NAME = path.abspath(path.join(path.dirname(__file__), 'primes-300k-to-400k.txt'))
BLOCK_SIZE = 2

def generate_pair():
    prime_list = open(PRIME_LIST_FILE_NAME).read().splitlines()
    p = int(random.choice(prime_list))
    g = random.randint(2, p - 1)
    x = random.randint(1, p - 2)
    y = modular_pow(g, x, p)

    public_key = (y, g, p)
    private_key = (x, p)
    return public_key, private_key

def encrypt(message, public_key):
    y, g, p = public_key
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
    x, p = private_key

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

if __name__ == '__main__':
    # Testing ground
    public_key, private_key = generate_pair()
    print('Public Key:', public_key)
    print('Private Key:', private_key)

    message = input('Message to be encrypted: ')
    encrypted = encrypt(message, public_key)
    decrypted = decrypt(encrypted, private_key)
    print('Encrypted message:', encrypted)
    print('Decrypted message:', decrypted)
