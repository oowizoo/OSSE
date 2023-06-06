import logging

# The file path of the database
DB_PATH = 'data/db.txt'

# The file path of the permutation key
PERMUTATION_KEY_PATH = 'data/pk.txt'

# The file path of the inverse permutation key
INVERSE_KEY_PATH = 'data/ik.txt'

# The bit length of the secret key components p and q
N = 128

# The security parameter lambda
LAMBDA = 128

# The logger object for logging messages
logger = logging.getLogger('OSSE')
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
