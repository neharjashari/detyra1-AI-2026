# Rezultatet - Problemi 3: Katrori latin

Gjeneruar me `python -m uninformed_search bench` më 2026-11-04 (Python 3.14.6, Darwin arm64).
Numri i nyjeve është deterministik për ekzekutimet që mbarojnë; për rreshtat 'limit' (kufiri i kohës 60 s) dhe për kohët rezultati varet nga shpejtësia e kompjuterit.

## 1. Madhësia e hapësirës së kërkimit

| n | qeliza n² | n^(n²) | (n!)^n | katrorë latinë L(n) | L(n) / n^(n²) |
|---|---|---|---|---|---|
| 1 | 1 | 1 | 1 | 1 | 10^0.0 |
| 2 | 4 | 16 | 4 | 2 | 10^-0.9 |
| 3 | 9 | 19,683 | 216 | 12 | 10^-3.2 |
| 4 | 16 | 4.29e9 | 331,776 | 576 | 10^-6.9 |
| 5 | 25 | 2.98e17 | 2.49e10 | 161,280 | 10^-12.3 |
| 6 | 36 | 1.03e28 | 1.39e17 | 8.13e8 | 10^-19.1 |
| 7 | 49 | 2.57e41 | 8.26e25 | 6.15e13 | 10^-27.6 |

L(n) nga OEIS A002860 (https://oeis.org/A002860).

## 2. IDDFS me backtracking

| n | statusi | iteracione | nyje gjithsej | nyje në iteracionin e fundit | gjithsej / e fundit | dead ends | koha (s) |
|---|---|---|---|---|---|---|---|
| 1 | solved | 2 | 1 | 1 | 1x | 0 | 0.000 |
| 2 | solved | 5 | 16 | 4 | 4x | 0 | 0.000 |
| 3 | solved | 10 | 316 | 10 | 32x | 19 | 0.000 |
| 4 | solved | 17 | 24,844 | 16 | 1,553x | 1,776 | 0.011 |
| 5 | solved | 26 | 13,505,897 | 37 | 365,024x | 1,717,327 | 6.907 |
| 6 | limit | 18 | 134,620,000 | - | - | 5,561,681 | 60.0 |

## 3. Nyjet për çdo iteracion të IDDFS, n = 5

| kufiri L | nyje të gjeneruara | rezultati |
|---|---|---|
| 0 | 0 | cutoff |
| 1 | 5 | cutoff |
| 2 | 25 | cutoff |
| 3 | 85 | cutoff |
| 4 | 205 | cutoff |
| 5 | 325 | cutoff |
| 6 | 805 | cutoff |
| 7 | 2,365 | cutoff |
| 8 | 6,205 | cutoff |
| 9 | 12,565 | cutoff |
| 10 | 17,845 | cutoff |
| 11 | 33,685 | cutoff |
| 12 | 73,285 | cutoff |
| 13 | 149,845 | cutoff |
| 14 | 250,645 | cutoff |
| 15 | 316,885 | cutoff |
| 16 | 449,365 | cutoff |
| 17 | 681,205 | cutoff |
| 18 | 1,012,405 | cutoff |
| 19 | 1,346,485 | cutoff |
| 20 | 1,507,765 | cutoff |
| 21 | 1,669,045 | cutoff |
| 22 | 1,830,325 | cutoff |
| 23 | 1,991,605 | cutoff |
| 24 | 2,152,885 | cutoff |
| 25 | 37 | solved |

```text
1 2 3 4 5
2 1 4 5 3
3 4 5 1 2
4 5 2 3 1
5 3 1 2 4
```
