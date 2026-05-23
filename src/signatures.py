from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization

# Global map acting as an in-memory database storing keys assigned to a username
WALLETS = {}

def get_or_create_wallet(username: str):
    if username not in WALLETS:
        # Creates a pair of private and public keys for digital identity
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        WALLETS[username] = {
            "private": private_key,
            "public": private_key.public_key()
        }
    return WALLETS[username]

def get_all_users() -> dict:
    users_info = {}
    for user, keys in WALLETS.items():
        # Export public key to a readable PEM format (standard format in cryptography)
        pem = keys["public"].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        users_info[user] = pem.decode('utf-8')
    return users_info

def sign_data(private_key, data: str) -> str:
    # Uses the private key to create a unique digital signature
    signature = private_key.sign(
        data.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    # Returns signature as a readable HEX string
    return signature.hex() 

def verify_signature(sender_username: str, signature_hex: str, data: str) -> bool:
    # Unknown public key for this sender
    if sender_username not in WALLETS:
        return False 
    
    public_key = WALLETS[sender_username]["public"]
    # Validates if the signature matches the data and the sender
    try:
        public_key.verify(
            bytes.fromhex(signature_hex),
            data.encode(),
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False