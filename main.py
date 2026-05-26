import os
from flask import Flask, render_template, request, jsonify, make_response
from src.blockchain import Blockchain
from src.block import Block
from src.transaction import Transaction
from src.signatures import get_or_create_wallet, sign_data, get_all_users
from src.community import COMMUNITY_USERS
from validators.hash_validator import validate_chain_hashes
from validators.signature_validator import validate_chain_signatures
from validators.structure_validator import validate_blockchain

app = Flask(__name__, template_folder='gui', static_folder='gui')
blockchain = Blockchain()
pending_transactions = []

@app.route('/')
def index():
    # Serve pure HTML template
    # Serwuje czysty szablon HTML
    return render_template('index.html')

@app.route('/api/community', methods=['GET'])
def get_community():
    # Return the allowed list of 10 popular Polish names
    # Zwraca dozwoloną listę 10 popularnych polskich imion
    return jsonify(COMMUNITY_USERS)

@app.route('/api/chain', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        # Manually reconstruct dict to include RSA signature for frontend
        # Ręcznie rekonstruuje słownik, aby dołączyć podpis RSA dla frontendu
        txs = []
        for tx in block.transactions:
            t_dict = tx.to_dict()
            t_dict['signature'] = tx.signature
            txs.append(t_dict)
            
        chain_data.append({
            'index': block.index,
            'timestamp': block.timestamp,
            'transactions': txs,
            'previous_hash': block.previous_hash,
            'nonce': block.nonce,
            'hash': block.hash
        })
    return jsonify(chain_data)

@app.route('/api/transaction', methods=['POST'])
def add_transaction():
    data = request.json
    sender = data.get('sender', '').strip()
    recipient = data.get('recipient', '').strip()
    
    if not sender or not recipient:
        return jsonify({"status": "error", "message": "Sender and recipient are required!"}), 400

    # Security: Validate if users belong to the predefined community
    # Bezpieczeństwo: Waliduje, czy użytkownicy należą do zdefiniowanej społeczności

    if sender not in COMMUNITY_USERS or recipient not in COMMUNITY_USERS:
        return jsonify({"status": "error", "message": "Users must belong to the allowed community!"}), 400

    if sender == recipient:
        return jsonify({"status": "error", "message": "Sender and recipient cannot be the same person!"}), 400

    # Prevent server crash by validating data type
    # Zapobiega awarii serwera poprzez walidację typu danych
    try:
        amount = float(data.get('amount'))
    except (ValueError, TypeError):
        return jsonify({"status": "error", "message": "Invalid transaction amount!"}), 400

    if amount <= 0:
        return jsonify({"status": "error", "message": "Amount must be strictly positive!"}), 400

    # Generate wallets if they do not exist
    # Generuje portfele, jeśli nie istnieją
    sender_wallet = get_or_create_wallet(sender)
    get_or_create_wallet(recipient)

    tx = Transaction(sender, recipient, amount)
    
    # Sign transaction with sender's private key
    # Podpisuje transakcję kluczem prywatnym nadawcy
    tx.signature = sign_data(sender_wallet['private'], str(tx.to_dict()))
    pending_transactions.append(tx)
    
    return jsonify({"status": "ok", "message": "Transaction added to queue"})

@app.route('/api/pending', methods=['GET'])
def get_pending():
    txs = [{"sender": tx.sender, "recipient": tx.recipient, "amount": tx.amount, "signature": tx.signature} 
           for tx in pending_transactions]
    return jsonify(txs)

@app.route('/api/mine', methods=['POST'])
def mine():
    global pending_transactions
    if not pending_transactions:
        return jsonify({"status": "error", "message": "No transactions to mine"}), 400
    
    new_block = Block(
        index=len(blockchain.chain),
        transactions=pending_transactions,
        previous_hash=blockchain.get_latest_block().hash
    )
    
    try:
        # Mine new block with Proof of Work
        # Kopie nowy blok za pomocą algorytmu Proof of Work
        blockchain.add_block(new_block, difficulty=2)
        # Clear pending queue after successful mining
        # Czyszczenie kolejki oczekujących transakcji po udanym wydobyciu
        pending_transactions = [] 
        return jsonify({"status": "ok", "message": "New block mined successfully!"})
    except ValueError as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/api/keys', methods=['GET'])
def get_keys():
    return jsonify(get_all_users())

@app.route('/api/validate/hash', methods=['GET'])
def val_hash():
    is_valid = validate_chain_hashes(blockchain)
    return jsonify({"valid": is_valid, "errors": [] if is_valid else ["Cryptographic hash consistency error."]})

@app.route('/api/validate/signature', methods=['GET'])
def val_sig():
    is_valid = validate_chain_signatures(blockchain)
    return jsonify({"valid": is_valid, "errors": [] if is_valid else ["Forged or missing signature detected in a block."]})

@app.route('/api/validate/structure', methods=['GET'])
def val_struct():
    result = validate_blockchain(blockchain)
    return jsonify(result)

@app.route('/api/reset', methods=['POST'])
def reset_chain():
    global blockchain, pending_transactions
    from src.signatures import WALLETS
    # Reset keys and chain
    # Resetuje klucze i łańcuch
    WALLETS.clear() 
    blockchain = Blockchain()
    pending_transactions = []
    return jsonify({"status": "ok", "message": "Blockchain reset"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)