# Blockchain Simulator

Symulator sieci blockchain z podpisami cyfrowymi RSA-2048, Proof of Work i walidacją integralności łańcucha.

## Wymagania

Python 3.11+

## Instalacja

```bash
pip install flask cryptography pytest
```

## Uruchomienie

```bash
python main.py
```

Następnie otwórz przeglądarkę i przejdź pod adres:

```
http://localhost:5000
```

## Uruchomienie testów

Z głównego folderu projektu:

```bash
python -m pytest tests/test_all.py -v
```

## Struktura projektu

```
blockchain-simulator/
├── main.py                  # Serwer Flask + REST API
├── src/                     # Logika kryptograficzna
│   ├── crypto_utils.py      # SHA-256, mod_pow, extended_gcd, Miller–Rabin
│   ├── signatures.py        # RSA-2048, podpisywanie PSS, weryfikacja
│   ├── transaction.py       # Model transakcji
│   ├── block.py             # Model bloku
│   ├── blockchain.py        # Łańcuch + Proof of Work
│   └── community.py        # Lista dozwolonych użytkowników
├── validators/              # Walidatory integralności
│   ├── hash_validator.py
│   ├── signature_validator.py
│   └── structure_validator.py
├── tests/
│   └── test_all.py          # 100 testów jednostkowych
├── gui/                     # Interfejs webowy
│   ├── index.html
│   ├── main.js
│   └── Style.css
├── conftest.py              # Konfiguracja pytest
└── pytest.ini
```