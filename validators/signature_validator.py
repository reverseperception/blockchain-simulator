from src.block import Block
from src.blockchain import Blockchain
from src.signatures import verify_signature

def validate_transaction_signature(tx) -> bool:
    # Unsigned transactions are rejected outright
    if tx.signature is None:
        return False

    return verify_signature(tx.sender, tx.signature, str(tx.to_dict()))

def validate_block_signatures(block: Block) -> bool:
    for tx in block.transactions:
        if not validate_transaction_signature(tx):
            return False
    return True

def validate_chain_signatures(blockchain: Blockchain) -> bool:
    # Genesis block has no transactions to verify
    for block in blockchain.chain[1:]:
        if not validate_block_signatures(block):
            return False
    return True