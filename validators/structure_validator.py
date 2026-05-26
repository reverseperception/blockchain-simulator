from src.block import Block
from src.blockchain import Blockchain
from src.transaction import Transaction
from validators.hash_validator import validate_chain_hashes
from validators.signature_validator import validate_chain_signatures

def validate_transaction_fields(tx) -> bool:
    # All three core fields must be present and non-empty
    # Wszystkie trzy kluczowe pola muszą być obecne i nie mogą być puste
    if not isinstance(tx, Transaction):
        return False
    if not tx.sender or not tx.recipient:
        return False
    if not isinstance(tx.amount, (int, float)) or tx.amount <= 0:
        return False
    return True

def validate_block_structure(block: Block) -> bool:
    required_attrs = ["index", "timestamp", "transactions", "previous_hash", "nonce", "hash"]

    for attr in required_attrs:
        if not hasattr(block, attr):
            return False

    if not isinstance(block.transactions, list):
        return False

    for tx in block.transactions:
        if not validate_transaction_fields(tx):
            return False

    return True

def validate_blockchain(blockchain: Blockchain) -> dict:
    errors = []

    # Genesis block must always exist
    # Blok genesis musi zawsze istnieć
    if not blockchain.chain:
        return {"valid": False, "errors": ["Chain is empty"]}

    # Check block structure and index ordering
    # Sprawdza strukturę bloku i kolejność indeksów
    for i, block in enumerate(blockchain.chain):
        if not validate_block_structure(block):
            errors.append(f"Block {i}: invalid structure")
        if block.index != i:
            errors.append(f"Block {i}: index mismatch (got {block.index})")

    # Delegate hash and signature checks to dedicated validators
    # Deleguje sprawdzanie hashu i podpisu do dedykowanych walidatorów
    if not validate_chain_hashes(blockchain):
        errors.append("Hash chain integrity compromised")

    if not validate_chain_signatures(blockchain):
        errors.append("One or more transaction signatures are invalid")

    return {"valid": len(errors) == 0, "errors": errors}