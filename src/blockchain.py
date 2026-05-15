from typing import List
from src.block import Block
from src.signatures import verify_signature
class Blockchain:
    def __init__(self):
    #internal ledger storage
        self.chain: List[Block] = []
        self.create_genesis_block()
    
    #Initializes the chain with a genesis block
    def create_genesis_block(self):
        genesis_block = Block(index=0, transactions=[], previous_hash="0")
        self.chain.append(genesis_block)

    #Helper for linking the next block
    def get_latest_block(self) -> Block:
        return self.chain[-1]
    
    def add_block(self, new_block: Block):
        # Validates all digital signatures within the block before insertion
        for tx in new_block.transactions:
            if not verify_signature(tx.sender, tx.signature, str(tx.to_dict())):
                raise ValueError("Security breach: Invalid transaction signature")

        # Logic for extending the chain
        new_block.previous_hash = self.get_latest_block().hash
        # Update hash after setting previous hash to maintain link
        new_block.hash = new_block.calculate_initial_hash()
        self.chain.append(new_block)