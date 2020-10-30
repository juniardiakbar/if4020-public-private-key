import random

from src.helper.math import modular_pow, gcd, xgcd, chooseE

def encrypt(message, key, block_size = 2):
    key_string = key.split(", ")
    n = int(key_string[0])
    e = int(key_string[1])

    encrypted_blocks = []
    ciphertext = -1

    if (len(message) > 0):
        ciphertext = ord(message[0])

    for i in range(1, len(message)):
        if (i % block_size == 0):
            encrypted_blocks.append(ciphertext)
            ciphertext = 0

        ciphertext = ciphertext * 1000 + ord(message[i])

    encrypted_blocks.append(ciphertext)

    for i in range(len(encrypted_blocks)):
        encrypted_blocks[i] = str(modular_pow(encrypted_blocks[i], e, n))

    encrypted_message = " ".join(encrypted_blocks)

    return encrypted_message

def decrypt(blocks, key, block_size = 2):
    key_string = key.split(", ")
    n = int(key_string[0])
    d = int(key_string[1])
    
    list_blocks = blocks.split(' ')
    int_blocks = []

    for s in list_blocks:
        int_blocks.append(int(s))

    message = ""

    for i in range(len(int_blocks)):
        int_blocks[i] = str(modular_pow(int_blocks[i], d, n))
        tmp = ""
        for c in range(block_size):
            tmp = chr(int_blocks[i] % 1000) + tmp
            int_blocks[i] //= 1000

        message += tmp

    return message

def generate_pair(public_key_path, private_key_path):
    rand1 = random.randint(100, 300)
    rand2 = random.randint(100, 300)

    fo = open('src/rsa/primes.txt', 'r')
    lines = fo.read().splitlines()
    fo.close()

    prime1 = int(lines[rand1])
    prime2 = int(lines[rand2])

    n = prime1 * prime2
    totient = (prime1 - 1) * (prime2 - 1)
    e = chooseE(totient)

    gcd, x, y = xgcd(e, totient)

    if (x < 0):
        d = x + totient
    else:
        d = x

    f_public = open(public_key_path, 'w')
    f_public.write(str(n) + ', ' + str(e))
    f_public.close()

    f_private = open(private_key_path, 'w')
    f_private.write(str(n) + ', ' + str(d))
    f_private.close()
