import time

class Transaction:

    # Store transaction details for ledger entry
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        # Unique timestamp prevents Replay Attacks
        self.timestamp = time.time()
        self.signature = None

    # Returns raw data for cryptographic process
    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
    
    # Debugging string format
    def __repr__(self) -> str:
        # Information about signature
        status = "Signed" if self.signature else "Unsigned"
        return f"{self.sender} to {self.recipient}: {self.amount} ({status})"