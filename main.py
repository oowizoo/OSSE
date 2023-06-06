import os
import sys
import argparse
import bitstring

from config import *
from utils import *
from osse import OSSE

def main():
    """
    The main function to run the OSSE evaluation.
    """
    # Parse the arguments
    parser = argparse.ArgumentParser(description='OSSE Evaluation')
    parser.add_argument('-d', '--db', type=str, default=DB_PATH, help='the file path of the database')
    parser.add_argument('-q', '--query', type=str, nargs='+', help='the query keywords')
    parser.add_argument('-t', '--test', action='store_true', help='whether to run the test mode')
    args = parser.parse_args()

    # Initialize the OSSE object
    osse = OSSE(args.db)

    # Setup the OSSE scheme
    edb, eidx = osse.setup()

    # Generate a query
    if args.query:
        q = args.query
    else:
        q = osse.db.get_random_query()
    c = osse.query(q)

    # Execute the query
    res = osse.execute(edb, eidx, c)

    # Print the results
    print(f'Query: {q}')
    print(f'Results: {res}')

if __name__ == '__main__':
    main()
