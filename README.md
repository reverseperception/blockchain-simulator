# Blockchain Simulator

Symulator sieci blockchain z podpisami cyfrowymi RSA-2048, Proof of Work i walidacją integralności łańcucha.

## Co robi

- **Podpisuje transakcje** kluczem prywatnym RSA-2048 (schemat PSS-SHA256) — każda transakcja jest kryptograficznie powiązana z nadawcą
- **Wydobywa bloki** algorytmem Proof of Work — SHA-256 z warunkiem na prefix, nonce inkrementowany do spełnienia warunku
- **Waliduje łańcuch** trzema niezależnymi walidatorami: integralność hashy, podpisy RSA, struktura bloków
- **Demonstruje atak** — modyfikacja kwoty w wydobytym bloku bez ponownego podpisywania, widoczne wykrycie przez walidatory
- **Implementuje od zera** trzy algorytmy matematyczne: szybkie potęgowanie modularne (square-and-multiply), rozszerzony algorytm Euklidesa, test pierwszości Millera–Rabina

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
│   └── community.py         # Lista dozwolonych użytkowników
├── validators/              # Walidatory integralności
│   ├── hash_validator.py
│   ├── signature_validator.py
│   └── structure_validator.py      
├── gui/                     # Interfejs webowy
│   ├── index.html
│   ├── main.js
│   └── Style.css
```