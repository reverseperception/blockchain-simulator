from src.block import Block
from src.blockchain import Blockchain


def validate_block_hash(block: Block) -> bool:
    # Recompute and compare against stored hash
    # Ponownie oblicza i porównuje z zapisanym hashem
    expected = block.calculate_initial_hash()
    return block.hash == expected


def validate_chain_hashes(blockchain: Blockchain) -> bool:
    chain = blockchain.chain

    for i in range(1, len(chain)):
        current = chain[i]
        previous = chain[i - 1]

        # Block's own hash must match its contents
        # Własny hash bloku musi zgadzać się z jego zawartością
        if not validate_block_hash(current):
            return False

        # Must point to the actual previous block
        # Musi wskazywać na faktyczny poprzedni blok
        if current.previous_hash != previous.hash:
            return False

    return True