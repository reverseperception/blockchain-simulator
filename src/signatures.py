from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization
from src.crypto_utils import miller_rabin, extended_gcd, mod_pow

# Global map acting as an in-memory database storing keys assigned to a username
# Globalna mapa działająca jako baza danych w pamięci, przechowująca klucze przypisane do nazwy użytkownika
WALLETS = {}

def get_or_create_wallet(username: str):
    if username not in WALLETS:
        # Creates a pair of private and public keys for digital identity
        # Tworzy parę kluczy prywatnego i publicznego dla cyfrowej tożsamości
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        WALLETS[username] = {
            "private": private_key,
            "public": private_key.public_key()
        }
        # Verify generated primes using our own Miller–Rabin implementation
        # Weryfikuje wygenerowane liczby pierwsze za pomocą własnej implementacji Millera–Rabina
        private_numbers = private_key.private_numbers()
        p, q = private_numbers.p, private_numbers.q
        assert miller_rabin(p, k=20), "Prime p failed Miller–Rabin verification"
        assert miller_rabin(q, k=20), "Prime q failed Miller–Rabin verification"

        # Verify RSA key relation: d * e ≡ 1 (mod φ(n)) using extended Euclid
        # Weryfikuje relację klucza RSA: d * e ≡ 1 (mod φ(n)) za pomocą rozszerzonego Euklidesa
        e = private_numbers.public_numbers.e
        phi_n = (p - 1) * (q - 1)
        gcd, _, _ = extended_gcd(e, phi_n)
        assert gcd == 1, "e and phi(n) are not coprime — key generation error"

        # Verify fast modular exponentiation: e^d mod n should recover original value
        # Weryfikuje szybkie potęgowanie modularne: e^d mod n powinno odtworzyć oryginalną wartość
        n = private_numbers.public_numbers.n
        d = private_numbers.d
        test_val = 42
        encrypted = mod_pow(test_val, e, n)
        decrypted = mod_pow(encrypted, d, n)
        assert decrypted == test_val, "Modular exponentiation round-trip failed"

    return WALLETS[username]

def get_all_users() -> dict:
    users_info = {}
    for user, keys in WALLETS.items():
        # Export public key to a readable PEM format (standard format in cryptography)
        # Eksportuje klucz publiczny do czytelnego formatu PEM (standardowy format w kryptografii)
        pem = keys["public"].public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        users_info[user] = pem.decode('utf-8')
    return users_info

def sign_data(private_key, data: str) -> str:
    # Uses the private key to create a unique digital signature
    # Używa klucza prywatnego do utworzenia unikalnego podpisu cyfrowego
    signature = private_key.sign(
        data.encode(),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    # Returns signature as a readable HEX string
    # Zwraca podpis w postaci czytelnego ciągu HEX
    return signature.hex()

def verify_signature(sender_username: str, signature_hex: str, data: str) -> bool:
    # Unknown public key for this sender
    # Nieznany klucz publiczny dla tego nadawcy
    if sender_username not in WALLETS:
        return False
    if not signature_hex:
        return False

    public_key = WALLETS[sender_username]["public"]
    # Validates if the signature matches the data and the sender
    # Sprawdza, czy podpis pasuje do danych i nadawcy
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