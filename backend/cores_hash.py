import os
from hashlib import blake2b
from base64 import b64encode, b64decode

def get_salt_hash(email, password):
    msg = bytes((email + password), 'utf-8')
    salt_bytes = os.urandom(blake2b.SALT_SIZE)
    salt_db_str = b64encode(salt_bytes).decode('utf-8')     
    hash = blake2b(salt=salt_bytes)
    hash.update(msg)
    hash_db_str = hash.hexdigest()                          
    return salt_db_str, hash_db_str

# The authenticate function does the following:
#   - generate the hash using the id, password and salt
#   - if (generated hash == hash stored in cores_db): return True
#   - else: return False 
def authenticate(email, password, salt_db_str, hash_db_str):
    
    # convert string id + password to bytes
    msg = bytes((email + password), 'utf-8')

    # convert salt from string to bytes
    salt_bytes = b64decode(salt_db_str)

    # Calculate the hash.  (blake2b.SALT_SIZE = 16)
    hash_check = blake2b(salt=salt_bytes)
    hash_check.update(msg)

    # convert hash to hex string
    hash_check_str = hash_check.hexdigest()

    # authenticate
    if hash_check_str == hash_db_str:
        return True
    else:
        return False