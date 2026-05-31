import hashlib
import json

# Standard SHA-256 hashing
# Standardowe hashowanie SHA-256
def get_sha256(data_string: str) -> str:
    return hashlib.sha256(data_string.encode()).hexdigest()

# Ensures deterministic hashing by sorting dictionary keys.
# Prevents different hashes for the same data due to key ordering.
# Zapewnia deterministyczne hashowanie poprzez sortowanie kluczy słownika.
# Zapobiega generowaniu różnych hashów dla tych samych danych z powodu kolejności kluczy.
def hash_block_data(block_dict: dict) -> str:
    encoded_block = json.dumps(block_dict, sort_keys=True).encode()
    return hashlib.sha256(encoded_block).hexdigest()

# Fast modular exponentiation using square-and-multiply algorithm (O log n)
# Szybkie potęgowanie modularne metodą „square-and-multiply" (złożoność O log n)
def mod_pow(base: int, exponent: int, modulus: int) -> int:
    if modulus == 1:
        return 0
    result = 1
    base = base % modulus
    while exponent > 0:
        # If current exponent bit is set, multiply into result
        # Jeśli aktualny bit wykładnika jest ustawiony, mnożymy do wyniku
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

# Extended Euclidean Algorithm — returns (gcd, x, y) such that a*x + b*y = gcd
# Rozszerzony algorytm Euklidesa — zwraca (nwd, x, y) takie że a*x + b*y = nwd
def extended_gcd(a: int, b: int) -> tuple:
    if a == 0:
        return b, 0, 1
    gcd, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return gcd, x, y

# Miller–Rabin primality test — probabilistic, k rounds reduce error to 4^(-k)
# Test pierwszości Millera–Rabina — probabilistyczny, k rund redukuje błąd do 4^(-k)
def miller_rabin(n: int, k: int = 20) -> bool:
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False

    # Write n-1 as 2^r * d
    # Zapisujemy n-1 jako 2^r * d
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    import random
    for _ in range(k):
        # Choose random witness a in [2, n-2]
        # Wybieramy losowego świadka a z przedziału [2, n-2]
        a = random.randrange(2, n - 1)
        x = mod_pow(a, d, n)

        if x == 1 or x == n - 1:
            continue

        composite = True
        for _ in range(r - 1):
            x = mod_pow(x, 2, n)
            if x == n - 1:
                composite = False
                break

        if composite:
            return False

    # Probably prime after k rounds
    # Prawdopodobnie pierwsza po k rundach
    return True