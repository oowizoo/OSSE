
import os
import random
import secrets
import bitstring

from config import *
from utils import *

class Obfuscation:
    """
    A class to implement random permutation for obfuscating access and search patterns.
    """

    def __init__(self):
        """
        Initialize the obfuscation class with the permutation key and the inverse key.
        """
        self.pk = self.load_key(PERMUTATION_KEY_PATH)
        self.ik = self.load_key(INVERSE_KEY_PATH)

    def load_key(self, path):
        """
        Load the permutation key or the inverse key from a file.

        Args:
            path (str): the file path of the key.

        Returns:
            list: a list of integers representing the key.
        """
        logger.info(f'Loading key from {path}...')
        timer.start()
        if os.path.exists(path):
            with open(path, 'r') as f:
                key = [int(x) for x in f.read().split()]
        else:
            logger.error(f'Key file not found: {path}')
            exit(1)
        timer.stop()
        logger.info(f'Key loaded in {timer.duration} seconds.')
        return key

    def generate_key(self, n):
        """
        Generate a random permutation key of size n and save it to a file.

        Args:
            n (int): the size of the key.

        Returns:
            list: a list of integers representing the key.
        """
        logger.info(f'Generating permutation key of size {n}...')
        timer.start()
        key = list(range(n))
        random.shuffle(key)
        with open(PERMUTATION_KEY_PATH, 'w') as f:
            f.write(' '.join(str(x) for x in key))
        timer.stop()
        logger.info(f'Permutation key generated and saved in {timer.duration} seconds.')
        return key

    def generate_inverse_key(self, pk):
        """
```python
Generate the inverse permutation key from a given permutation key and save it to a file.

Args:
    pk (list): a list of integers representing the permutation key.

Returns:
    list: a list of integers representing the inverse key.
"""
        logger.info('Generating inverse permutation key...')
        timer.start()
        n = len(pk)
        ik = [0] * n
        for i in range(n):
            ik[pk[i]] = i
        with open(INVERSE_KEY_PATH, 'w') as f:
            f.write(' '.join(str(x) for x in ik))
        timer.stop()
        logger.info(f'Inverse permutation key generated and saved in {timer.duration} seconds.')
        return ik
