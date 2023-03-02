import hashlib
from typing import List


def const_hash(value, len: int = 10):
    hash_object = hashlib.sha1(str(value).encode())

    # Get the hexadecimal representation of the hash
    hex_dig = hash_object.hexdigest()

    # Convert the hexadecimal representation to an integer
    int_hash = int(hex_dig, 16) % (10 ** len)
    return int_hash


def const_hash_arr(values: List, len: int = 10):
    ret = 1
    for val in values:
        ret = (ret * const_hash(val, len)) % (10 ** len)
    return ret
