import hashlib
import json
 
# Standard SHA-256 hashing
def get_sha256(data_string: str) -> str:
    return hashlib.sha256(data_string.encode()).hexdigest()

# Ensures deterministic hashing by sorting dictionary keys.
# Prevents different hashes for the same data due to key ordering.
def hash_block_data(block_dict: dict) -> str:
    encoded_block = json.dumps(block_dict, sort_keys=True).encode()
    return hashlib.sha256(encoded_block).hexdigest()