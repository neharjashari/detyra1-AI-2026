# Rezultatet - Problemi 2: Sudoku

Gjeneruar me `python -m uninformed_search bench` më 2026-11-04 (Python 3.14.6, Darwin arm64).
Numri i nyjeve është deterministik për ekzekutimet që mbarojnë; për rreshtat 'limit' (kufiri i kohës 60 s) dhe për kohët rezultati varet nga shpejtësia e kompjuterit.

## BFS me backtracking për të gjitha enigmat

| niveli | enigma | dhëna | bosh (k) | 9^k | çdo rresht permutacion | statusi | nyje të gjeneruara | nyje të zgjeruara | dead ends | radha max | koha (s) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| easy | euler-01 | 32 | 49 | 5.73e46 | 7.80e21 | solved | 928 | 928 | 274 | 146 | 0.001 |
| easy | euler-02 | 30 | 51 | 4.64e48 | 5.62e23 | solved | 2,169 | 2,169 | 658 | 235 | 0.003 |
| medium | euler-03 | 28 | 53 | 3.76e50 | 1.38e25 | solved | 22,918 | 22,918 | 6,674 | 3,616 | 0.036 |
| medium | euler-07 | 26 | 55 | 3.04e52 | 1.27e27 | solved | 16,164 | 16,164 | 4,867 | 2,212 | 0.025 |
| hard | euler-06 | 24 | 57 | 2.47e54 | 6.34e28 | solved | 181,883 | 181,883 | 65,346 | 49,303 | 0.311 |
| hard | euler-26 | 24 | 57 | 2.47e54 | 2.08e28 | solved | 12,876 | 12,876 | 3,704 | 1,395 | 0.020 |
| hard | inkala-2012 | 21 | 60 | 1.80e57 | 6.99e30 | solved | 2,068,780 | 2,068,780 | 705,261 | 356,812 | 3.249 |
