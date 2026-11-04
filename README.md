# Detyra 1: Kërkimi i painformuar (Inteligjenca Artificiale 2026/27)

**Lënda:** Inteligjenca Artificiale · Master, Inxhinieri Kompjuterike dhe Softuerike ·
FIEK, Universiteti i Prishtinës

**Detyra:** [Detyra e parë semestrale](https://github.com/adrianymeri/Artificial-Intelligence-2026/blob/main/Detyra1.md)

Implementim në Python i katër problemeve të detyrës. Për problemet 1-3 secili dokument ndjek
kërkesat e detyrës: modelimi, reprezentimi (variablat, domenet, kufizimet), funksioni objektiv,
landscape (madhësia e hapësirës së kërkimit) dhe algoritmi i kërkuar i kërkimit të painformuar.

| # | Problemi | Algoritmi i kërkuar | Rezultati kryesor | Dokumentimi |
|---|---|---|---|---|
| 1 | Social Golfers (32 lojtarë, grupe me 4) | DFS + backtracking | Maksimumi është **10 javë** (kufi i vërtetuar me numërim + orar i njohur në literaturë); DFS gjen 5 javë menjëherë | [docs/01-social-golfers.md](docs/01-social-golfers.md) |
| 2 | Sudoku (Easy / Medium / Hard) | BFS + backtracking | Të 7 enigmat zgjidhen; më e vështira (Inkala 2012) në ≈ 3 s | [docs/02-sudoku.md](docs/02-sudoku.md) |
| 3 | Latin Square (`n × n`) | IDDFS + backtracking | `n = 5` në ≈ 7 s; analizë pse IDDFS përsërit shumë punë këtu | [docs/03-latin-square.md](docs/03-latin-square.md) |
| 4 | Pemët e kërkimit: 8-Puzzle, Misionarët & Kanibalët, Rotating Workforce Scheduling | BFS / DFS (tree & graph search) | 6 pemë të gjeneruara automatikisht (SVG) | [docs/04-search-trees.md](docs/04-search-trees.md) |

## Struktura

```text
detyra1/
├── uninformed_search/
│   ├── social_golfers.py       # Problemi 1: DFS me backtracking
│   ├── sudoku.py               # Problemi 2: BFS me backtracking
│   ├── latin_square.py         # Problemi 3: IDDFS me backtracking
│   ├── trees/                  # Problemi 4: pemët e kërkimit + eksporti Graphviz
│   │   ├── core.py             #   ndërtimi i pemës (BFS/DFS, tree/graph search)
│   │   ├── eight_puzzle.py
│   │   ├── missionaries.py
│   │   └── rotating_workforce.py
│   ├── experiments.py          # eksperimentet që gjenerojnë results/*.md
│   ├── common.py               # statistikat e kërkimit, kufiri i kohës, formatimi
│   └── cli.py                  # CLI
├── data/sudoku/                # enigmat easy / medium / hard
├── docs/                       # përshkrimi i secilit problem + figurat (docs/img)
├── results/                    # tabelat e rezultateve (të gjeneruara)
└── tests/                      # testet (pytest)
```

## Instalimi

Kërkohet **Python ≥ 3.10**. Kodi nuk ka varësi të jashtme.

```bash
git clone https://github.com/neharjashari/detyra1-AI-2026.git detyra1 && cd detyra1
python3 -m venv .venv && source .venv/bin/activate     # opsionale
pip install -r requirements-dev.txt                    # vetëm për testet (pytest)
```

Për të rigjeneruar figurat e pemëve nevojitet [Graphviz](https://graphviz.org/download/)
(`brew install graphviz` / `sudo apt install graphviz`). Figurat SVG janë tashmë në `docs/img/`.

## Ekzekutimi

```bash
python -m uninformed_search --help

# Problemi 1: Social Golfers
python -m uninformed_search golfers -w 5                 # 8-4-5 me DFS
python -m uninformed_search golfers --max-weeks          # w = 1, 2, ... derisa DFS të ndalet
python -m uninformed_search golfers -w 10 --landscape    # madhësia e hapësirës së kërkimit

# Problemi 2: Sudoku
python -m uninformed_search sudoku                       # të gjitha nivelet
python -m uninformed_search sudoku --level hard
# enigmë e dhënë si 81 karaktere, rresht pas rreshti ('.' ose '0' = qelizë bosh)
python -m uninformed_search sudoku --puzzle "..3.2.6..9..3.5..1..18.64....81.29..7.......8..67.82....26.95..8..2.3..9..5.1.3.."

# Problemi 3: Latin Square
python -m uninformed_search latin -n 5                   # IDDFS
python -m uninformed_search latin -n 4 -v                # me nyjet e çdo iteracioni

# Problemi 4: Pemët e kërkimit
python -m uninformed_search trees                        # rigjeneron docs/img/*.svg (kërkon Graphviz)
python -m uninformed_search trees --ascii mc_bfs_graph   # pema në terminal

# Të gjitha eksperimentet (≈ 3 min) → results/*.md
python -m uninformed_search bench

# Testet
python -m pytest
```
