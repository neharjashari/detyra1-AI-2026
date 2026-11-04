"""Runs all experiments and writes the tables in results/*.md (`bench` command)."""

from __future__ import annotations

import math
import platform
import time
from datetime import date
from pathlib import Path

from . import latin_square as latin
from . import social_golfers as golf
from . import sudoku
from .common import sci

TIME_LIMIT = 60.0


def table(headers: list[str], rows: list[list]) -> str:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(out)


def header(title: str) -> str:
    return (
        f"# {title}\n\n"
        f"Gjeneruar me `python -m uninformed_search bench` më {date.today().isoformat()} "
        f"(Python {platform.python_version()}, {platform.system()} {platform.machine()}).\n"
        "Numri i nyjeve është deterministik për ekzekutimet që mbarojnë; për rreshtat 'limit' "
        f"(kufiri i kohës {TIME_LIMIT:.0f} s) dhe për kohët rezultati varet nga shpejtësia e kompjuterit.\n"
    )


def fmt_time(seconds: float) -> str:
    return f"{seconds:.3f}" if seconds < 10 else f"{seconds:.1f}"


def golfers_report() -> str:
    parts = [header("Rezultatet - Problemi 1: Social Golfers")]

    parts.append("## 1. Madhësia e hapësirës së kërkimit për 32 lojtarë (8 grupe me 4), w javë\n")
    rows = []
    for w in range(1, 11):
        land = golf.landscape(8, 4, w)
        rows.append(
            [
                w,
                sci(land["every_slot_any_player"]),
                sci(land["every_week_a_permutation"]),
                sci(land["every_week_a_partition"]),
            ]
        )
    parts.append(
        table(
            ["w", "32^(32·w): çdo vend çdo lojtar", "(32!)^w: çdo javë permutacion", "P^w: çdo javë ndarje"],
            rows,
        )
    )
    land = golf.landscape(8, 4, 10)
    parts.append(
        f"\nP = ndarjet e 32 lojtarëve në 8 grupe me nga 4 = {land['partitions_of_one_week']:,}. "
        f"Çifte lojtarësh: {land['pairs_of_players']}, çifte që takohen në një javë: {land['pairs_per_week']}, "
        f"kufiri i sipërm: {land['upper_bound_weeks']} javë.\n"
    )

    parts.append("## 2. DFS me backtracking për 32 lojtarë, w = 1, 2, ...\n")
    results = golf.max_weeks_dfs(8, 4, TIME_LIMIT)
    rows = [
        [
            w,
            res.status,
            f"{res.stats.nodes_generated:,}",
            f"{res.stats.nodes_expanded:,}",
            f"{res.stats.dead_ends:,}",
            res.stats.max_depth,
            fmt_time(res.stats.elapsed),
        ]
        for w, res in results
    ]
    parts.append(
        table(
            [
                "w",
                "statusi",
                "nyje të gjeneruara",
                "nyje të zgjeruara",
                "dead ends",
                "thellësia max",
                "koha (s)",
            ],
            rows,
        )
    )

    parts.append("\n## 3. DFS me backtracking për instanca të vogla\n")
    rows = []
    for g, p, w in [(2, 2, 3), (3, 2, 5), (3, 3, 4), (4, 3, 4), (4, 4, 5), (5, 5, 6), (2, 4, 2)]:
        res = golf.solve_dfs(g, p, w, TIME_LIMIT)
        rows.append(
            [
                f"{g}-{p}-{w}",
                g * p,
                golf.max_weeks(g, p),
                res.status,
                f"{res.stats.nodes_generated:,}",
                f"{res.stats.dead_ends:,}",
                fmt_time(res.stats.elapsed),
            ]
        )
    parts.append(
        table(
            ["g-p-w", "lojtarë", "kufiri i sipërm", "statusi", "nyje të gjeneruara", "dead ends", "koha (s)"],
            rows,
        )
    )

    best = [(w, res) for w, res in results if res.status == "solved"][-1]
    parts.append(f"\n## 4. Orari i gjetur nga DFS për {best[0]} javë\n")
    parts.append(f"```text\n{golf.format_schedule(best[1].schedule)}\n```")
    return "\n".join(parts) + "\n"


def sudoku_report() -> str:
    parts = [header("Rezultatet - Problemi 2: Sudoku")]
    parts.append("## BFS me backtracking për të gjitha enigmat\n")
    rows = []
    for level in sudoku.LEVELS:
        for name, puzzle in sudoku.load_puzzles(level):
            land = sudoku.landscape(puzzle)
            res = sudoku.solve_bfs(puzzle, time_limit=TIME_LIMIT)
            rows.append(
                [
                    level,
                    name,
                    land["givens"],
                    land["empty_cells"],
                    sci(land["any_digit_in_every_empty_cell"]),
                    sci(land["every_row_a_permutation"]),
                    res.status,
                    f"{res.stats.nodes_generated:,}",
                    f"{res.stats.nodes_expanded:,}",
                    f"{res.stats.dead_ends:,}",
                    f"{res.stats.max_frontier:,}",
                    fmt_time(res.stats.elapsed),
                ]
            )
    parts.append(
        table(
            [
                "niveli",
                "enigma",
                "dhëna",
                "bosh (k)",
                "9^k",
                "rreshtat permutacione",
                "statusi",
                "nyje të gjeneruara",
                "nyje të zgjeruara",
                "dead ends",
                "radha max",
                "koha (s)",
            ],
            rows,
        )
    )
    return "\n".join(parts) + "\n"


def latin_report() -> str:
    parts = [header("Rezultatet - Problemi 3: Katrori latin")]

    parts.append("## 1. Madhësia e hapësirës së kërkimit\n")
    rows = []
    for n in range(1, 8):
        land = latin.landscape(n)
        share = math.log10(land["latin_squares"]) - math.log10(land["any_value_in_every_cell"])
        rows.append(
            [
                n,
                land["cells"],
                sci(land["any_value_in_every_cell"]),
                sci(land["every_row_a_permutation"]),
                sci(land["latin_squares"]),
                f"10^{share:.1f}",
            ]
        )
    parts.append(table(["n", "qeliza n²", "n^(n²)", "(n!)^n", "katrorë latinë L(n)", "L(n) / n^(n²)"], rows))
    parts.append("\nL(n) nga OEIS A002860 (https://oeis.org/A002860).\n")

    parts.append("## 2. IDDFS me backtracking\n")
    rows = []
    for n in range(1, 7):
        res = latin.solve_iddfs(n, time_limit=TIME_LIMIT)
        last = res.iterations[-1].nodes if res.status == "solved" else None
        rows.append(
            [
                n,
                res.status,
                len(res.iterations),
                f"{res.stats.nodes_generated:,}",
                "-" if last is None else f"{last:,}",
                "-" if last is None else f"{res.stats.nodes_generated / last:,.0f}x",
                f"{res.stats.dead_ends:,}",
                fmt_time(res.stats.elapsed),
            ]
        )
    parts.append(
        table(
            [
                "n",
                "statusi",
                "iteracione",
                "nyje gjithsej",
                "nyje në iteracionin e fundit",
                "gjithsej / e fundit",
                "dead ends",
                "koha (s)",
            ],
            rows,
        )
    )

    parts.append("\n## 3. Nyjet për çdo iteracion të IDDFS, n = 5\n")
    res = latin.solve_iddfs(5, time_limit=TIME_LIMIT)
    parts.append(
        table(
            ["kufiri L", "nyje të gjeneruara", "rezultati"],
            [[i.limit, f"{i.nodes:,}", i.result] for i in res.iterations],
        )
    )
    parts.append(f"\n```text\n{latin.format_square(res.square)}\n```")
    return "\n".join(parts) + "\n"


def trees_report(img_dir: Path) -> str:
    from . import trees
    from .trees.eight_puzzle import reachable_states
    from .trees.missionaries import MissionariesCannibals, state_space
    from .trees.rotating_workforce import RotatingWorkforce, search_space

    parts = [header("Rezultatet - Problemi 4: Pemët e kërkimit")]
    summary = trees.render_all(img_dir)
    rows = [
        [
            name,
            s["nodes"],
            s["expanded"],
            s["per_depth"],
            s["avg_branching"],
            "-" if s["solution_depth"] is None else s["solution_depth"],
            " ".join(s["solution"]) if s["solution"] else "-",
        ]
        for name, s in summary.items()
    ]
    parts.append(
        table(
            [
                "figura",
                "nyje",
                "të zgjeruara",
                "nyje për thellësi",
                "degëzimi mesatar",
                "thellësia",
                "zgjidhja",
            ],
            rows,
        )
    )

    layers = reachable_states()
    parts.append(
        "\n## 8-Puzzle\n\n"
        f"* Gjendje të arritshme nga qëllimi (BFS mbi tërë hapësirën): {sum(layers.values()):,} (= 9!/2); "
        f"distanca maksimale: {max(layers)}.\n"
        f"* Gjendje sipas distancës nga qëllimi: {layers}\n"
    )
    mc = state_space(MissionariesCannibals())
    parts.append(
        "\n## Misionarët dhe Kanibalët\n\n"
        f"* Treshe (m, c, b): {mc['all']}, të vlefshme: {mc['valid']}, "
        f"të arritshme nga fillimi: {mc['reachable']}.\n"
    )
    rws = search_space(RotatingWorkforce())
    parts.append(
        "\n## Rotating Workforce Scheduling\n\n"
        f"* Veprime për nivel (ditë): {rws['actions_per_level']}; gjethe të pemës kolonë-pas-kolone: "
        f"{rws['leaves_column_wise']:,}; përfaqësim qelizë-pas-qelize: 3^21 = {rws['cell_wise']:,}.\n"
    )
    return "\n".join(parts) + "\n"


def run_all(out_dir: Path, img_dir: Path) -> None:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    jobs = [
        ("01-social-golfers.md", golfers_report),
        ("02-sudoku.md", sudoku_report),
        ("03-latin-square.md", latin_report),
        ("04-search-trees.md", lambda: trees_report(img_dir)),
    ]
    for name, job in jobs:
        start = time.perf_counter()
        (out_dir / name).write_text(job(), encoding="utf-8")
        print(f"{name}: {time.perf_counter() - start:.1f} s")
