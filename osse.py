import os
import math
import random
import secrets
import bitstring

from config import *
from utils import *
from database import Database
from encryption import Encryption
from obfuscation import Obfuscation

class OSSE:
    """
    A class to implement Obfuscated Searchable Symmetric Encryption (OSSE) scheme.
    """

    def __init__(self, db_path):
        """
        Initialize the OSSE class with the database, the encryption and the obfuscation objects.

        Args:
            db_path (str): the file path of the database.
        """
        # Create a database object with the given file path
        self.db = Database(db_path)
        # Create an encryption object with the IPPE scheme
        self.enc = Encryption()
        # Create an obfuscation object with the random permutation
        self.obf = Obfuscation()
        # Get the bit length of the keywords from the encryption object
        self.n = self.enc.n
        # Get the bit length of the secret parameter q from the encryption object
        self.m = self.enc.m
        # Get the security parameter lambda from the encryption object
        self.l = LAMBDA // 8

    def setup(self):
        """
        ```python

        Setup the OSSE scheme by encrypting the database and generating the index.

        Returns:
        list: a list of ciphertexts representing the encrypted database.
        dict: a dictionary mapping keywords to ciphertexts representing the encrypted index.
        """
        # Log the message of setting up OSSE scheme
        logger.info('Setting up OSSE scheme...')
        # Start the timer
        timer.start()
        # Initialize an empty list of encrypted documents
        edb = []
        # Initialize an empty dictionary of encrypted index
        eidx = {}
        # For each document id and document in the database
        for doc_id, doc in enumerate(self.db.docs):
        # Convert the document to a bit vector using the database object
            x = self.db.doc_to_vector(doc)
        # Encrypt the bit vector using the encryption object
            c = self.enc.encrypt(x)
        # Append the ciphertext to the encrypted database list
            edb.append(c)
        # For each keyword in the document
            for w in doc:
        # If the keyword is not in the encrypted index dictionary
                if w not in eidx:
        # Initialize an empty bit array for the keyword
                    eidx[w] = bitstring.BitArray()
        # Append the document id to the bit array of the keyword
                eidx[w].append(doc_id)
        # For each keyword in the encrypted index dictionary
        for w in eidx:
        # Encrypt the bit array of the keyword using the encryption object
            eidx[w] = self.enc.encrypt(eidx[w])
        # Stop the timer
        timer.stop()
        # Log the message of OSSE scheme set up with the elapsed time
        logger.info(f'OSSE scheme set up in {timer.duration} seconds.')
        # Return the encrypted database list and encrypted index dictionary
        return edb, eidx

    def query(self, q):
        """
        Generate a query for a conjunctive keyword search using OSSE scheme.

        Args:
        q (list): a list of keywords representing the query.

        Returns:
        bitstring.BitArray: a ciphertext representing the encrypted query.
        """
        # Check if the query is not empty
        assert len(q) > 0, 'Invalid query'
        # Log the message of generating query for q
        logger.info(f'Generating query for {q}...')
        # Start the timer
        timer.start()

        # Convert the query to a bit vector using the database object
        x = self.db.query_to_vector(q)
        # Encrypt the bit vector using the encryption object
        c = self.enc.encrypt(x)
        # Stop the timer
        timer.stop()
        # Log the message of query generated with the elapsed time
        logger.info(f'Query generated in {timer.duration} seconds.')
        # Return c as the encrypted query
        return c

    def execute(self, edb, eidx, c):
        """
        Execute a query on an encrypted database and index using OSSE scheme.

        Args:
            edb (list): a list of ciphertexts representing the encrypted database.
            eidx (dict): a dictionary mapping keywords to ciphertexts representing the encrypted index.
            c (bitstring.BitArray): a ciphertext representing the encrypted query.

        Returns:
            list: a list of document ids representing the matching results.
        """
        # Log the message of executing query on edb and eidx
        logger.info('Executing query on edb and eidx...')
        # Start the timer
        timer.start()
        # Initialize an empty list of matching results
        res = []
        # For each document id and ciphertext in edb
        for doc_id, c1 in enumerate(edb):
            # Compute the inner product of c and c1 using the encryption object
            d = self.enc.ip(c, c1)
            # If the inner product is 0
            if d == 0:
            # Append the document id to the matching results list
                res.append(doc_id)
        # Generate a random permutation key of size len(edb) using the obfuscation object
        pk = self.obf.generate_key(len(edb))
        # Get the inverse permutation key from the obfuscation object
        ik = self.obf.ik
        # For each index in the matching results list
        for i in range(len(res)):
            # Replace the document id with the permuted document id using pk
            res[i] = pk[res[i]]
        # Stop the timer
        timer.stop()
        # Log the message of query executed with the elapsed time and the number of results
        logger.info(f'Query executed in {timer.duration} seconds. {len(res)} results found.')
        # Return res as the matching results list
        return res

