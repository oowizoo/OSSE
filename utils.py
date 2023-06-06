import time
import math
import bitstring

class Timer:
    """
    A class to measure the elapsed time.
    """

    def __init__(self):
        """
        Initialize the timer class with the start and end time.
        """
        # Set the start time and end time to None
        self.start_time = None
        self.end_time = None

    def start(self):
        """
        Start the timer.
        """
        # Get the current time as the start time
        self.start_time = time.time()

    def stop(self):
        """
        Stop the timer.
        """
        # Get the current time as the end time
        self.end_time = time.time()

    @property
    def duration(self):
        """
        Get the duration of the timer in seconds.

        Returns:
            float: the duration in seconds.
        """
        # Return the difference between the end time and the start time as the duration
        return self.end_time - self.start_time

# Create a global timer object
timer = Timer()

def is_prime(n):
    """
    Check if a number n is prime using Miller-Rabin primality test.

    Args:
        n (int): a number to be checked.

    Returns:
        bool: True if n is prime, False otherwise.
    """
    # If n is 2 or 3, return True
    if n == 2 or n == 3:
        return True
    # If n is less than 2 or even, return False
    if n < 2 or n % 2 == 0:
        return False
    # Find r and s such that n - 1 = 2^r * s and s is odd
    r, s = 0, n - 1
    while s % 2 == 0:
        r += 1
        s //= 2
    # Repeat 10 times
    for _ in range(10):
        # Choose a random number a between 2 and n - 2
        a = random.randrange(2, n - 1)
        # Compute x = a^s mod n
        x = pow(a, s, n)
        # If x is 1 or n - 1, continue
        if x == 1 or x == n - 1:
            continue
        # Repeat r - 1 times
        for _ in range(r - 1):
            # Compute x = x^2 mod n
            x = pow(x, 2, n)
            # If x is n - 1, break
            if x == n - 1:
                break
        else:
            # Return False
            return False
    # Return True
    return True

def bitarray_to_int(x):
    """
    Convert a bit array to an integer.

    Args:
    x (bitstring.BitArray): a bit array.

    Returns:
    int: an integer. 
    """
    # Return the integer representation of the binary string of x
    return int(x.bin, 2)

def int_to_bitarray(x, length=None):
    """
    Convert an integer to a bit array.

    Args:
    x (int): an integer.
    length (int): the length of the bit array. If None, use the minimum length.

    Returns:
    bitstring.BitArray: a bit array. 
    """
    # If length is None, use the minimum length to represent x in binary
    if length is None:
        length = math.ceil(math.log2(x + 1))
    # Return the bit array representation of x with the given length
    return bitstring.BitArray(uint=x, length=length)
