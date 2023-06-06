import os
import math
import random
import secrets
import hashlib
import bitstring
from Crypto.Cipher import AES
from Crypto.Util import Counter

from config import *
from utils import *

class Encryption:
    """
    A class to implement Inner Product Predicate Encryption (IPPE) scheme.
    """

    def __init__(self):
        """
        Initialize the encryption class with the secret key and the public parameters.
        """
        # Generate the secret key p and q
        self.sk = self.keygen()
        # Get the public parameter p
        self.p = self.sk['p']
        # Get the public parameter q
        self.q = self.sk['q']
        # Get the bit length of p
        self.n = math.ceil(math.log2(self.p))
        # Get the bit length of q
        self.m = math.ceil(math.log2(self.q))
        # Get the security parameter lambda
        self.l = LAMBDA // 8

    def keygen(self):
        """
        Generate the secret key for IPPE scheme.

        Returns:
            dict: a dictionary containing the secret key components p and q.
        """
        # Log the message of generating secret key
        logger.info('Generating secret key...')
        # Start the timer
        timer.start()
        # Generate a random N-bit number p
        p = secrets.randbits(N)
        # Generate a random N-bit number q
        q = secrets.randbits(N)

        # Repeat until both p and q are prime numbers
        while not (is_prime(p) and is_prime(q)):
            # Generate a new random N-bit number p
            p = secrets.randbits(N)
            # Generate a new random N-bit number q
            q = secrets.randbits(N)
        # Stop the timer
        timer.stop()
        # Log the message of secret key generated with the elapsed time
        logger.info(f'Secret key generated in {timer.duration} seconds.')
        # Return the secret key as a dictionary with p and q as keys
        return {'p': p, 'q': q}

def encrypt(self, x):
    """
    Encrypt a bit vector x using IPPE scheme.

    Args:
        x (bitstring.BitArray): a bit vector of length n.

    Returns:
        bitstring.BitArray: a ciphertext of length m * n + l.
    """
    # Check if the input length is equal to n
    assert len(x) == self.n, 'Invalid input length'
    # Generate a random number r between 0 and q - 1
    r = secrets.randbelow(self.q)
    # Initialize an empty bit array y
    y = bitstring.BitArray()
    # For each bit in x
    for i in range(self.n):
        # Append (r * x[i] + a random number between 0 and p - 1) modulo q to y
        y.append((r * x[i] + secrets.randbelow(self.p)) % self.q)
    # Generate a random l-byte string k
    k = bitstring.BitArray(os.urandom(self.l))
    # Compute c as y XOR F(k, x), where F is a pseudorandom function
    c = y ^ self.F(k, x)
    # Append k to c
    c.append(k)
    # Return c as the ciphertext
    return c

def decrypt(self, c):
    """
    Decrypt a ciphertext c using IPPE scheme.

    Args:
        c (bitstring.BitArray): a ciphertext of length m * n + l.

    Returns:
        bitstring.BitArray: a bit vector of length n.
    """


    # Check if the ciphertext length is equal to m * n + l
    assert len(c) == self.m * self.n + self.l, 'Invalid ciphertext length'
    # Get y as the first m * n bits of c
    y = c[:self.m * self.n]
    # Get k as the last l bits of c
    k = c[self.m * self.n:]
    # Initialize an empty bit array x
    x = bitstring.BitArray()
    # For each m-bit segment in y
    for i in range(self.n):
        # Append ((y[i] XOR F(k, i)) modulo p) modulo 2 to x, where F is a pseudorandom function and i is an index in [0, n)
        x.append((y[i * self.m : (i + 1) * self.m] ^ self.F(k, i)) % self.p % 2)
    # Return x as the plaintext
    return x

def ip(self, c1, c2):
    """
    Compute the inner product of two ciphertexts c1 and c2 using IPPE scheme.

    Args:
        c1 (bitstring.BitArray): a ciphertext of length m * n + l.
        c2 (bitstring.BitArray): a ciphertext of length m * n + l.

    Returns:
        int: the inner product of the plaintexts modulo p.
    """
    # Check if the ciphertext lengths are equal to m * n + l
    assert len(c1) == len(c2) == self.m * self.n + self.l, 'Invalid ciphertext length'
    # Get y1 as the first m * n bits of c1
    y1 = c1[:self.m * self.n]
    # Get k1 as the last l bits of c1
    k1 = c1[self.m * self.n:]
    # Get y2 as the first m * n bits of c2
    y2 = c2[:self.m * self.n]
    # Get k2 as the last l bits of c2
    k2 = c2[self.m * self.n:]
    # Compute z as y1 XOR y2
    z = y1 ^ y2
    # Compute s as k1 XOR k2
    s = k1 ^ k2
    # Initialize d as 0
    d = 0


    # For each m-bit segment in z
    for i in range(self.n):
        # Add ((z[i] XOR F(s, i)) modulo q) to d, where F is a pseudorandom function and i is an index in [0, n)
        d += (z[i * self.m : (i + 1) * self.m] ^ self.F(s, i)) % self.q
    # Return d modulo p as the inner product
    return d % self.p

def F(self, k, x):
    """
    A pseudorandom function F that maps a key k and an input x to an output of length m.

    Args:
        k (bitstring.BitArray): a key of length l.
        x (bitstring.BitArray or int): an input of length n or an index in [0, n).

    Returns:
       bitstring.BitArray: an output of length m. 
    """
    # If x is an integer, convert it to a bit array of length n
    if isinstance(x, int):
       x = bitstring.BitArray(uint=x, length=self.n)
    # Check if the input lengths are valid
    assert len(k) == self.l and len(x) == self.n, 'Invalid input length'
    # Initialize an AES cipher with k as the key and counter mode as the mode of operation
    aes = AES.new(k.bytes, AES.MODE_CTR, counter=Counter.new(128))
    # Encrypt x using the AES cipher and get the first m bits as the output
    return bitstring.BitArray(aes.encrypt(x.bytes))[:self.m]
