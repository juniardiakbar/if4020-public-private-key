from helper import modular_pow

def encrypt(message, block_size = 2):
    n = 1568953
    e = 339575

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

def decrypt(blocks, block_size = 2):
    n = 1568953
    d = 545303

    list_blocks = blocks.split(' ')
    int_blocks = []

    for s in list_blocks:
        int_blocks.append(int(s))

    message = ""

    for i in range(len(int_blocks)):
        int_blocks[i] = (int_blocks[i]**d) % n
        tmp = ""
        for c in range(block_size):
            tmp = chr(int_blocks[i] % 1000) + tmp
            int_blocks[i] //= 1000

        message += tmp

    return message
