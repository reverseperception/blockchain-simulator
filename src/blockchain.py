from typing import List
from src.block import Block

class Blockchain:
    def __init__(self):
        # Internal ledger storage
        self.chain: List[Block] = []
        self.create_genesis_block()
    
    # Initializes the chain with a genesis block
    def create_genesis_block(self):
        genesis_block = Block(index=0, transactions=[], previous_hash="0")
        self.chain.append(genesis_block)

    # Helper for linking the next block
    def get_latest_block(self) -> Block:
        return self.chain[-1]
        
    # Calculates user balance based on the entire chain history
    def get_balance(self, user: str) -> float:
        balance = 0.0
        for block in self.chain:
            for tx in block.transactions:
                if tx.sender == user:
                    balance -= tx.amount
                if tx.recipient == user:
                    balance += tx.amount
        return balance
    
    def add_block(self, new_block: Block, difficulty: int = 2):
        # Validates all digital signatures within the block before insertion
        from validators.signature_validator import validate_block_signatures
        if not validate_block_signatures(new_block):
            raise ValueError("Security breach: Invalid transaction signature")
        
        new_block.previous_hash = self.get_latest_block().hash
        
        # PROOF OF WORK: search for a hash starting with a specific number of zeros
        target = "0" * difficulty
        new_block.hash = new_block.calculate_initial_hash()
        
        while not new_block.hash.startswith(target):
            new_block.nonce += 1
            new_block.hash = new_block.calculate_initial_hash()
            
        # Update hash after setting previous hash to maintain link
        self.chain.append(new_block)