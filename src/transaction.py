import time

class Transaction:

    # Store transaction details for ledger entry
    # Przechowuje szczegóły transakcji do wpisu w księdze głównej
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        # Unique timestamp prevents Replay Attacks
        # Unikalny znacznik czasu (timestamp) zapobiega atakom typu Replay Attack (atakom powtórzeniowym)
        self.timestamp = time.time()
        self.signature = None

    # Returns raw data for cryptographic process
    # Zwraca surowe dane do procesu kryptograficznego
    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount,
            "timestamp": self.timestamp
        }
    
    # Debugging string format
    # Format ciągu znaków do celów debugowania
    def __repr__(self) -> str:
        # Information about signature
        # Informacja o podpisie
        status = "Signed" if self.signature else "Unsigned"
        return f"{self.sender} to {self.recipient}: {self.amount} ({status})"