# Rezultatet - Problemi 1: Social Golfers

Gjeneruar me `python -m uninformed_search bench` më 2026-11-04 (Python 3.14.6, Darwin arm64).
Numri i nyjeve është deterministik për ekzekutimet që mbarojnë; për rreshtat 'limit' (kufiri i kohës 60 s) dhe për kohët rezultati varet nga shpejtësia e kompjuterit.

## 1. Madhësia e hapësirës së kërkimit për 32 lojtarë (8 grupe me 4), w javë

| w | 32^(32·w): çdo vend çdo lojtar | (32!)^w: çdo javë permutacion | P^w: çdo javë ndarje |
|---|---|---|---|
| 1 | 1.46e48 | 2.63e35 | 5.93e19 |
| 2 | 2.14e96 | 6.92e70 | 3.51e39 |
| 3 | 3.12e144 | 1.82e106 | 2.08e59 |
| 4 | 4.56e192 | 4.79e141 | 1.24e79 |
| 5 | 6.67e240 | 1.26e177 | 7.32e98 |
| 6 | 9.75e288 | 3.32e212 | 4.34e118 |
| 7 | 1.42e337 | 8.73e247 | 2.57e138 |
| 8 | 2.08e385 | 2.30e283 | 1.53e158 |
| 9 | 3.04e433 | 6.05e318 | 9.05e177 |
| 10 | 4.45e481 | 1.59e354 | 5.37e197 |

P = ndarjet e 32 lojtarëve në 8 grupe me nga 4 = 59,287,247,761,257,140,625. Çifte lojtarësh: 496, çifte që takohen në një javë: 48, kufiri i sipërm: 10 javë.

## 2. DFS me backtracking për 32 lojtarë, w = 1, 2, ...

| w | statusi | nyje të gjeneruara | nyje të zgjeruara | dead ends | thellësia max | koha (s) |
|---|---|---|---|---|---|---|
| 1 | solved | 32 | 32 | 0 | 31 | 0.000 |
| 2 | solved | 64 | 64 | 0 | 63 | 0.000 |
| 3 | solved | 96 | 96 | 0 | 95 | 0.000 |
| 4 | solved | 128 | 128 | 0 | 127 | 0.000 |
| 5 | solved | 160 | 160 | 0 | 159 | 0.000 |
| 6 | limit | 55,530,000 | 55,530,000 | 26,096,103 | 163 | 60.0 |

## 3. DFS me backtracking për instanca të vogla

| g-p-w | lojtarë | kufiri i sipërm | statusi | nyje të gjeneruara | dead ends | koha (s) |
|---|---|---|---|---|---|---|
| 2-2-3 | 4 | 3 | solved | 12 | 0 | 0.000 |
| 3-2-5 | 6 | 5 | solved | 36 | 3 | 0.000 |
| 3-3-4 | 9 | 4 | solved | 37 | 1 | 0.000 |
| 4-3-4 | 12 | 5 | solved | 407 | 141 | 0.000 |
| 4-4-5 | 16 | 5 | solved | 80 | 0 | 0.000 |
| 5-5-6 | 25 | 6 | solved | 2,246 | 1,218 | 0.003 |
| 2-4-2 | 8 | 2 | failure | 519 | 252 | 0.000 |

## 4. Orari i gjetur nga DFS për 5 javë

```text
Java  1:   0  1  2  3  |   4  5  6  7  |   8  9 10 11  |  12 13 14 15  |  16 17 18 19  |  20 21 22 23  |  24 25 26 27  |  28 29 30 31
Java  2:   0  4  8 12  |   1  5  9 13  |   2  6 10 14  |   3  7 11 15  |  16 20 24 28  |  17 21 25 29  |  18 22 26 30  |  19 23 27 31
Java  3:   0  5 10 15  |   1  4 11 14  |   2  7  8 13  |   3  6  9 12  |  16 21 26 31  |  17 20 27 30  |  18 23 24 29  |  19 22 25 28
Java  4:   0  6 11 13  |   1  7 10 12  |   2  4  9 15  |   3  5  8 14  |  16 22 27 29  |  17 23 26 28  |  18 20 25 31  |  19 21 24 30
Java  5:   0  7  9 14  |   1  6  8 15  |   2  5 11 12  |   3  4 10 13  |  16 23 25 30  |  17 22 24 31  |  18 21 27 28  |  19 20 26 29
```
