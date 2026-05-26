import time
from typing import List, Optional
from src.transaction import Transaction
from src.crypto_utils import hash_block_data

class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str, nonce: int = 0):
        self.index = index  # Position of the block in the chain # Pozycja bloku w łańcuchu
        self.timestamp = time.time()  # Block creation timestamp # Znacznik czasu utworzenia bloku
        self.transactions = transactions  # List of transactions included in the block # Lista transakcji zawartych w bloku
        self.previous_hash = previous_hash  # Hash of the previous block # Hash poprzedniego bloku
        self.nonce = nonce  # Counter adjusted during mining to find a hash for Proof of Work # Licznik modyfikowany podczas kopania, aby znaleźć hash spełniający warunki Proof of Work
        self.hash = self.calculate_initial_hash()  # Initial hash calculation upon block instantiation # Początkowe wyliczenie hasha podczas tworzenia instancji bloku

    # Generates the cryptographic SHA-256 fingerprint of the block
    # Generuje kryptograficzny odcisk palca SHA-256 dla bloku
    def calculate_initial_hash(self) -> str:
        block_content = {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [tx.to_dict() for tx in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        return hash_block_data(block_content)

    # Returns a technical summary of the block for debugging
    # Zwraca techniczny podsumowanie bloku do debugowania
    def __repr__(self):
        return f"Block(Index: {self.index}, Hash: {self.hash[:10]}...)"