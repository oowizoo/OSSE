import os
import math
import random
import secrets
import bitstring

from config import *
from utils import *

class Database:
    """
    A class to represent a database of documents and keywords.
    """

    def __init__(self, db_path):
        """
        Initialize the database class with the documents and the keywords.

        Args:
            db_path (str): the file path of the database.
        """
        # Load the documents from the file
        self.docs = self.load_docs(db_path)
        # Get the unique keywords from the documents
        self.keywords = self.get_keywords()
        # Get the bit length of the keywords
        self.n = len(self.keywords)
        # Get a mapping from keywords to indices
        self.w2i = {w: i for i, w in enumerate(self.keywords)}

    def load_docs(self, db_path):
        """
        Load the documents from a file.

        Args:
            db_path (str): the file path of the database.

        Returns:
            list: a list of lists of keywords representing the documents.
        """

        # Log the message of loading documents
        logger.info(f'Loading documents from {db_path}...')
        # Start the timer
        timer.start()
        # If the file exists
        if os.path.exists(db_path):
            # Open the file in read mode
            with open(db_path, 'r') as f:
                # Read each line and split it by whitespace to get a list of keywords
                docs = [line.strip().split() for line in f]
        # Otherwise
        else:
            # Log the error message of file not found
            logger.error(f'Database file not found: {db_path}')
            # Exit the program
            exit(1)
        # Stop the timer
        timer.stop()
        # Log the message of documents loaded with the elapsed time and the number of documents
        logger.info(f'{len(docs)} documents loaded in {timer.duration} seconds.')
        # Return the list of documents
        return docs

    def get_keywords(self):
        """
        Get the unique keywords from the documents.

        Returns:
            list: a list of keywords sorted alphabetically.
        """
        # Log the message of getting unique keywords
        logger.info('Getting unique keywords...')
        # Start the timer
        timer.start()
        # Initialize an empty set of keywords
        keywords = set()
        # For each document in the database
        for doc in self.docs:
            # Add all the keywords in the document to the set
            keywords.update(doc)
        # Convert the set to a sorted list
        keywords = sorted(keywords)


        # Stop the timer
        timer.stop()
        # Log the message of unique keywords obtained with the elapsed time and the number of keywords
        logger.info(f'{len(keywords)} unique keywords obtained in {timer.duration} seconds.')
        # Return the list of keywords
        return keywords

    def doc_to_vector(self, doc):
        """
        Convert a document to a bit vector.

        Args:
            doc (list): a list of keywords representing a document.

        Returns:
        bitstring.BitArray: a bit vector of length n. 
        """
        # Initialize an empty bit vector x
        x = bitstring.BitArray()
        # For each keyword in the keyword list
        for w in self.keywords:
            # If the keyword is in the document, append 1 to x, otherwise append 0 to x
            x.append(w in doc)
        # Return x as the bit vector
        return x

    def query_to_vector(self, q):
        """

    Convert a query to a bit vector.

    Args:
    q (list): a list of keywords representing a query.

    Returns:
    bitstring.BitArray: a bit vector of length n. 
    """
    # Initialize an empty bit vector x
        x = bitstring.BitArray()
        # For each keyword in the keyword list
        for w in self.keywords:
        # If the keyword is in the query, append 1 to x, otherwise append 0 to x
            x.append(w in q)
        # Return x as the bit vector
        return x

    def get_random_query(self):
        """
        Get a random query from the database.

        Returns:
        list: a list of keywords representing a query.
        """
        # Choose a random document from the database
        doc = random.choice(self.docs)
        # Choose a random number k between 1 and len(doc)
        k = random.randint(1, len(doc))
        # Choose k random keywords from doc as the query
        q = random.sample(doc, k)
        # Return q as the query
        return q