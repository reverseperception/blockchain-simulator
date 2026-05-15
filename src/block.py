import time
from typing import List, Optional
from src.transaction import Transaction

class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str, nonce: int = 0):
        self.index = index  # Position of the block in the chain
        self.timestamp = time.time()  # Block creation timestamp
        self.transactions = transactions  # List of transactions included in the block
        self.previous_hash = previous_hash  # Hash of the previous block
        self.nonce = nonce  # Counter adjusted during mining to find a hash for Proof of Work
        self.hash = self.calculate_initial_hash()  # Initial hash calculation upon block instantiation

    def calculate_initial_hash(self) -> str:
        # TODO: Implement hash calculation using crypto_utilities
        return ""

    def __repr__(self):
        return f"Block(Index: {self.index}, Hash: {self.hash[:10]}...)"