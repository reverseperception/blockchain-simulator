document.addEventListener('DOMContentLoaded', () => {
    // Handle navigation menu clicks
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', (e) => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
            
            e.target.classList.add('active');
            document.getElementById(`page-${e.target.dataset.page}`).classList.add('active');
            refreshData();
        });
    });

    // Helper function to append action logs to the UI
    function log(msg, type="info") {
        const logEl = document.getElementById('log-el');
        const time = new Date().toLocaleTimeString();
        logEl.innerHTML += `<div class="log-line"><span class="log-time">[${time}]</span> <span class="log-${type}">${msg}</span></div>`;
        logEl.scrollTop = logEl.scrollHeight;
    }

    // Fetch and render the entire blockchain state from the server
    async function refreshData() {
        const res = await fetch('/api/chain');
        const chain = await res.json();
        
        document.getElementById('s-blocks').innerText = chain.length;
        let txCount = chain.reduce((acc, block) => acc + block.transactions.length, 0);
        document.getElementById('s-txs').innerText = txCount;

        const chainEl = document.getElementById('chain-el');
        chainEl.innerHTML = '';
        
        const atkSelect = document.getElementById('atk-block');
        atkSelect.innerHTML = '';

        chain.forEach(block => {
            // Render individual block in the chain visualization
            const b = document.createElement('div');
            b.className = 'block';
            b.innerHTML = `
                <div class="block-top"></div>
                <div class="block-body">
                    <div class="block-row"><span>Blok</span><span>#${block.index}</span></div>
                    <div class="block-hash">${block.hash}</div>
                    <div class="block-tag ${block.index === 0 ? 'tag-genesis' : 'tag-tx'}">
                        ${block.index === 0 ? 'Genesis' : block.transactions.length + ' tx'}
                    </div>
                </div>
            `;
            b.onclick = () => showBlockDetails(block);
            chainEl.appendChild(b);

            // Add connecting arrows between blocks
            if(block.index < chain.length - 1) {
                const arrow = document.createElement('div');
                arrow.className = 'chain-arrow';
                arrow.innerText = '→';
                chainEl.appendChild(arrow);
            }

            // Populate block selection dropdown for data tampering attack (excluding Genesis)
            if(block.index > 0 && block.transactions.length > 0) {
                atkSelect.innerHTML += `<option value="${block.index}">Blok #${block.index}</option>`;
            }
        });
        
        refreshPending();
        refreshKeys();
    }

    // Fetch and render the pending transactions pool
    async function refreshPending() {
        const res = await fetch('/api/pending');
        const pending = await res.json();
        const el = document.getElementById('pending-el');
        
        if (pending.length === 0) {
            el.innerHTML = '<p class="hint">Brak transakcji w kolejce</p>';
            return;
        }
        
        el.innerHTML = pending.map(tx => `
            <div class="pending-item" style="flex-direction: column; align-items: flex-start; gap: 8px;">
                <div style="display: flex; justify-content: space-between; width: 100%;">
                    <div class="pending-name">${tx.sender} → ${tx.recipient}</div>
                    <div class="pending-amt">${tx.amount} BTC</div>
                </div>
                <div class="pending-sig" style="font-size: 10px; color: #6e6e73; word-break: break-all;">Podpis:<br>${tx.signature}</div>
            </div>
        `).join('');
    }

    // Fetch and render the list of users and their RSA public keys
    async function refreshKeys() {
        const res = await fetch('/api/keys');
        const users = await res.json();
        const el = document.getElementById('users-list');
        
        if (Object.keys(users).length === 0) {
            el.innerHTML = '<p class="hint">Brak użytkowników — dodaj transakcję</p>';
            return;
        }
        
        el.innerHTML = Object.keys(users).map(user => `
            <div class="user-item" style="flex-direction: column; align-items: flex-start; gap: 8px;">
                <div style="display: flex; justify-content: space-between; width: 100%;">
                    <div class="user-name">${user}</div>
                    <div class="user-badge">Klucz publiczny RSA</div>
                </div>
                <div class="d-val mono" style="font-size: 10px; background: #f5f5f7; padding: 12px; border-radius: 6px; width: 100%;">
                    ${users[user].replace(/\n/g, '<br>')}
                </div>
            </div>
        `).join('');
    }

    // Display selected block details in the side panel
    function showBlockDetails(block) {
        document.getElementById('detail-empty').style.display = 'none';
        document.getElementById('detail-panel').style.display = 'grid';
        
        document.getElementById('d-header').innerHTML = `
            <div class="d-field"><div class="d-label">Index</div><div class="d-val">${block.index}</div></div>
            <div class="d-field"><div class="d-label">Nonce (Proof of Work)</div><div class="d-val">${block.nonce}</div></div>
            <div class="d-field"><div class="d-label">Hash</div><div class="d-val mono">${block.hash}</div></div>
            <div class="d-field"><div class="d-label">Poprzedni Hash</div><div class="d-val mono">${block.previous_hash}</div></div>
        `;

        const txsEl = document.getElementById('d-txs');
        if(block.transactions.length === 0) {
            txsEl.innerHTML = '<p class="hint">Brak transakcji (Genesis Block)</p>';
        } else {
            txsEl.innerHTML = block.transactions.map(tx => `
                <div class="tx-item" style="flex-direction: column; align-items: flex-start; gap: 8px;">
                    <div style="display: flex; justify-content: space-between; width: 100%;">
                        <div class="tx-name">${tx.sender} → ${tx.recipient}</div>
                        <div class="tx-amt">${tx.amount} BTC</div>
                    </div>
                    <div class="tx-sig mono" style="font-size: 10px; color: #6e6e73; word-break: break-all;">Podpis (RSA-PSS):<br>${tx.signature ? tx.signature : 'Brak'}</div>
                </div>
            `).join('');
        }
    }

    // Handle new transaction submission
    document.getElementById('btn-add-tx').onclick = async () => {
        const s = document.getElementById('tx-sender').value;
        const r = document.getElementById('tx-recipient').value;
        const a = document.getElementById('tx-amount').value;
        
        if(!s || !r || !a) {
            document.getElementById('tx-msg').innerText = "Wypełnij wszystkie pola!";
            document.getElementById('tx-msg').className = "msg err";
            return;
        }
        
        let response;
        try {
            response = await fetch('/api/transaction', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({sender: s, recipient: r, amount: a})
            });
        } catch (e) {
            document.getElementById('tx-msg').innerText = "Brak połączenia z serwerem.";
            document.getElementById('tx-msg').className = "msg err";
            return;
        }
        
        let data;
        try {
            // Parse server response safely
            data = await response.json();
        } catch(e) {
            // Generic fallback for critical server errors (HTTP 500)
            document.getElementById('tx-msg').innerText = "Krytyczny błąd serwera (Internal Server Error). Sprawdź logi.";
            document.getElementById('tx-msg').className = "msg err";
            return;
        }
        
        // Handle server-side validation feedback
        if (data.status === "ok") {
            document.getElementById('tx-msg').innerText = "Dodano do kolejki!";
            document.getElementById('tx-msg').className = "msg ok";
            document.getElementById('tx-amount').value = '';
            log(`Dodano transakcję ${s} -> ${r} (${a} BTC)`, "info");
        } else {
            document.getElementById('tx-msg').innerText = data.message;
            document.getElementById('tx-msg').className = "msg err";
            log(`Odrzucono transakcję: ${data.message}`, "err");
        }
        
        refreshPending();
    };

    // Handle Proof of Work mining process
    document.getElementById('btn-mine').onclick = async () => {
        document.getElementById('mine-pow').style.display = 'block';
        document.getElementById('mine-msg').innerText = '';
        
        let res, data;
        try {
            res = await fetch('/api/mine', {method: 'POST'});
            data = await res.json();
        } catch(e) {
            document.getElementById('mine-pow').style.display = 'none';
            document.getElementById('mine-msg').className = "msg err";
            document.getElementById('mine-msg').innerText = "Błąd serwera podczas kopania.";
            return;
        }
        
        document.getElementById('mine-pow').style.display = 'none';
        
        if(data.status === "ok") {
            document.getElementById('mine-msg').className = "msg ok";
            document.getElementById('mine-msg').innerText = data.message;
            log(`Wykopano nowy blok!`, "ok");
            refreshData();
        } else {
            document.getElementById('mine-msg').className = "msg err";
            document.getElementById('mine-msg').innerText = data.message;
        }
    };

    // Execute specific blockchain validation algorithms
    async function runValidator(endpoint, elId) {
        const res = await fetch(endpoint);
        const data = await res.json();
        const el = document.getElementById(elId);
        
        if(data.valid) {
            el.innerHTML = `<div class="result ok"><div class="result-title">Sukces</div>Wszystkie testy zaliczone.</div>`;
            log(`Walidacja ${endpoint.split('/').pop()} zakończona pomyślnie.`, "ok");
            document.getElementById('s-status').className = 'status-ok';
            document.getElementById('s-status').innerText = '● Prawidłowy';
        } else {
            el.innerHTML = `<div class="result err"><div class="result-title">Błąd Walidacji</div>` + 
                           data.errors.map(e => `<div class="result-row">${e}</div>`).join('') + `</div>`;
            log(`Wykryto błąd podczas walidacji ${endpoint.split('/').pop()}!`, "err");
            document.getElementById('s-status').className = 'status-err';
            document.getElementById('s-status').innerText = '● Naruszony';
        }
    }

    // Event listeners for validator buttons
    document.getElementById('btn-val-hash').onclick = () => runValidator('/api/validate/hash', 'val-hash-result');
    document.getElementById('btn-val-sig').onclick = () => runValidator('/api/validate/signature', 'val-sig-result');
    document.getElementById('btn-val-struct').onclick = () => runValidator('/api/validate/structure', 'val-struct-result');

    // Handle simulated attack (Data Tampering) on the blockchain
    document.getElementById('btn-attack').onclick = async () => {
        const idx = document.getElementById('atk-block').value;
        const amt = document.getElementById('atk-amount').value;
        
        if(!idx || !amt) return;
        
        await fetch('/api/attack', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({block_idx: idx, amount: amt})
        });
        
        document.getElementById('atk-result').innerHTML = `<div class="result err">Transakcja w bloku #${idx} została sfałszowana. Uruchom walidatory!</div>`;
        log(`Przeprowadzono atak na blok #${idx}!`, "warn");
        refreshData();
    };

    // Reset blockchain state and clear in-memory wallets
    document.getElementById('btn-reset').onclick = async () => {
        await fetch('/api/reset', {method: 'POST'});
        log(`Blockchain został zresetowany.`, "info");
        document.getElementById('atk-result').innerHTML = '';
        document.querySelectorAll('.result').forEach(el => el.innerHTML = '');
        document.getElementById('tx-msg').innerText = ''; 
        document.getElementById('mine-msg').innerText = '';
        refreshData();
    };

    // Initialize the application data on load
    refreshData();
});