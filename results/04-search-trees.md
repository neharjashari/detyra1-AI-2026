# Rezultatet - Problemi 4: Pemët e kërkimit

Gjeneruar me `python -m uninformed_search bench` më 2026-11-04 (Python 3.14.6, Darwin arm64).
Numri i nyjeve është deterministik për ekzekutimet që mbarojnë; për rreshtat 'limit' (kufiri i kohës 60 s) dhe për kohët rezultati varet nga shpejtësia e kompjuterit.

| figura | nyje | të zgjeruara | nyje për thellësi | degëzimi mesatar | thellësia | zgjidhja |
|---|---|---|---|---|---|---|
| 8puzzle_full_depth3 | 36 | 12 | [1, 3, 8, 24] | 2.92 | - | - |
| 8puzzle_bfs_graph | 54 | 20 | [1, 3, 8, 15, 24, 3] | 2.65 | 5 | ↑ ↑ ← ↓ → |
| mc_bfs_graph | 47 | 13 | [1, 5, 6, 5, 2, 4, 5, 5, 4, 2, 5, 3] | 3.54 | 11 | 2K 1K 2K 1K 2M 1M1K 2M 1K 2K 1M 1M1K |
| mc_dfs_ancestors | 33 | 13 | [1, 4, 2, 4, 4, 2, 5, 2, 3, 2, 1, 3] | 2.46 | 11 | 2K 1K 2K 1K 2M 1M1K 2M 1K 2K 1M 1M1K |
| rws_full_depth2 | 43 | 7 | [1, 6, 36] | 6.0 | - | - |
| rws_dfs | 70 | 15 | [1, 1, 1, 3, 6, 12, 13, 33] | 4.6 | 7 | -DN -DN D-N ND- ND- -DN D-N |

## 8-Puzzle

* Gjendje të arritshme nga qëllimi (BFS mbi tërë hapësirën): 181,440 (= 9!/2); distanca maksimale: 30.
* Gjendje sipas distancës nga qëllimi: {0: 1, 1: 4, 2: 8, 3: 8, 4: 16, 5: 32, 6: 60, 7: 72, 8: 136, 9: 200, 10: 376, 11: 512, 12: 964, 13: 1296, 14: 2368, 15: 3084, 16: 5482, 17: 6736, 18: 11132, 19: 12208, 20: 18612, 21: 18444, 22: 24968, 23: 19632, 24: 22289, 25: 13600, 26: 11842, 27: 4340, 28: 2398, 29: 472, 30: 148}


## Misionarët dhe Kanibalët

* Treshe (m, c, b): 32, të vlefshme: 20, të arritshme nga fillimi: 16.


## Rotating Workforce Scheduling

* Veprime për nivel (ditë): [6, 6, 6, 6, 6, 6, 6]; gjethe të pemës kolonë-pas-kolone: 279,936; reprezentim qelizë-pas-qelize: 3^21 = 10,460,353,203.

