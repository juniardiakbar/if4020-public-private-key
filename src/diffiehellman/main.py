from math import sqrt
from src.helper.math import modular_pow

def is_prime(x):
    for i in range(2, int(sqrt(x))):
        if x % i == 0:
            return False
    return True

def generate_symmetric_key(n, g, x, y):
    if not is_prime(n):
        raise ValueError('n must be prime')
    if not g < n:
        raise ValueError('g must be lower than n')
    
    X = modular_pow(g, x, n)
    Y = modular_pow(g, y, n)

    K_Alice = modular_pow(Y, x, n)
    K_Bob = modular_pow(X, y, n)

    if K_Alice != K_Bob:
        raise RuntimeError('Returned symmetric keys differ from each other')
    return K_Alice
