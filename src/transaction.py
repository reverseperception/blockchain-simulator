class Transaction:

    # Store transaction details for ledger entry
    def __init__(self, sender: str, recipient: str, amount: float):
        self.sender=sender
        self.recipient = recipient
        self.amount = amount
        self.signature = None

    # Returns raw data for cryptographic process
    def to_dict(self):
        return {
            "sender": self.sender,
            "recipient": self.recipient,
            "amount": self.amount
        }
    
    # Debugging string format
    def __repr__(self) -> str:
        #Information about signature
        status = "Signed" if self.signature else "Unsigned"
        return str(self.sender) + " to " + str(self.recipient) + ": " + str(self.amount)