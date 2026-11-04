"""CLI: python -m uninformed_search <golfers|sudoku|latin|trees|bench> [options]"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from . import latin_square as latin
from . import social_golfers as golf
from . import sudoku, trees
from .common import sci

ROOT = Path(__file__).resolve().parent.parent


def _print_stats(stats) -> None:
    print("Statistikat:", json.dumps(stats.as_dict(), ensure_ascii=False))


def _print_landscape(values: dict) -> None:
    for key, value in values.items():
        print(f"  {key:>32}: {sci(value) if isinstance(value, int) else value}")


def _positive(value: str) -> int:
    number = int(value)
    if number < 1:
        raise argparse.ArgumentTypeError("duhet të jetë numër i plotë pozitiv")
    return number


def _group_size(value: str) -> int:
    number = int(value)
    if number < 2:
        raise argparse.ArgumentTypeError("madhësia e grupit duhet të jetë të paktën 2")
    return number


def _puzzle(value: str) -> str:
    try:
        grid = sudoku.parse(value)
    except ValueError:
        raise argparse.ArgumentTypeError("duhen saktësisht 81 qeliza (1-9, 0 ose . për bosh)") from None
    if sudoku.has_conflicts(grid):
        raise argparse.ArgumentTypeError("dhënat përsërisin një shifër në rresht, kolonë ose kuti")
    return grid


# problem 1
def cmd_golfers(args: argparse.Namespace) -> int:
    g, p, w = args.groups, args.size, args.weeks
    print(
        f"Social Golfers: {g * p} lojtarë, {g} grupe me nga {p}; kufiri i sipërm = {golf.max_weeks(g, p)} javë"
    )

    if args.landscape:
        print(f"Hapësira e kërkimit (landscape) për {g}-{p}-{w}:")
        _print_landscape(golf.landscape(g, p, w))
        return 0

    if args.max_weeks:
        results = golf.max_weeks_dfs(g, p, args.time_limit)
        for weeks, res in results:
            print(f"  w={weeks:>2}: {res.status:<8} {res.stats.as_dict()} {res.reason}")
        solved = [(weeks, res) for weeks, res in results if res.status == "solved"]
        if solved:
            weeks, res = solved[-1]
            print(f"\nDFS gjeti orar për {weeks} javë:")
            print(golf.format_schedule(res.schedule))
        return 0

    res = golf.solve_dfs(g, p, w, args.time_limit)
    print(f"Instanca {g}-{p}-{w}: {res.status} {res.reason}")
    _print_stats(res.stats)
    if res.schedule:
        print(golf.format_schedule(res.schedule))
        print("I vlefshëm:", golf.is_valid(res.schedule, g, p), "| f =", golf.objective(res.schedule))
    return 0 if res.status == "solved" else 1


# problem 2
def cmd_sudoku(args: argparse.Namespace) -> int:
    if args.puzzle:
        puzzles = [("input", args.puzzle)]
    else:
        levels = sudoku.LEVELS if args.level == "all" else (args.level,)
        puzzles = [(f"{lvl}/{name}", grid) for lvl in levels for name, grid in sudoku.load_puzzles(lvl)]

    exit_code = 0
    for name, puzzle in puzzles:
        givens = 81 - puzzle.count(".")
        print(f"\n=== {name}  (dhëna: {givens}, niveli: {sudoku.level_of(puzzle)}) ===")
        print(sudoku.format_grid(puzzle))
        if args.landscape:
            _print_landscape(sudoku.landscape(puzzle))
        res = sudoku.solve_bfs(puzzle, time_limit=args.time_limit)
        print(f"BFS: {res.status} {res.reason}")
        _print_stats(res.stats)
        if res.solution:
            print(sudoku.format_grid(res.solution))
            print("Zgjidhje e vlefshme:", sudoku.is_solution(res.solution, puzzle))
        else:
            exit_code = 1
    return exit_code


# problem 3
def cmd_latin(args: argparse.Namespace) -> int:
    n = args.n
    if args.landscape:
        print(f"Hapësira e kërkimit (landscape) për n = {n}:")
        _print_landscape(latin.landscape(n))
        return 0

    res = latin.solve_iddfs(n, time_limit=args.time_limit)
    print(f"Katrori latin n={n} (IDDFS): {res.status} {res.reason}")
    _print_stats(res.stats)
    if args.verbose:
        print("Iteracionet (kufiri L -> nyje të gjeneruara):")
        for it in res.iterations:
            print(f"  L={it.limit:>3}: {it.nodes:>12,}  {it.result}")
    if res.square:
        print(latin.format_square(res.square))
        print("I vlefshëm:", latin.is_latin_square(res.square), "| f =", latin.objective(res.square))
    return 0 if res.status == "solved" else 1


# problem 4
def cmd_trees(args: argparse.Namespace) -> int:
    if args.ascii:
        tree, title, _ = trees.build_figure(args.ascii)
        print(title)
        print(trees.ascii_tree(tree))
        print(json.dumps(tree.stats(), ensure_ascii=False))
        if isinstance(tree.problem, trees.RotatingWorkforce) and tree.goal:
            from .trees.rotating_workforce import format_schedule

            print("\nOrari i gjetur:")
            print(format_schedule(tree.problem, tree.goal.state))
        return 0
    summary = trees.render_all(Path(args.out), fmt=args.format)
    for name, stats in summary.items():
        print(f"{name:<22} nyje={stats['nodes']:<4} thellësia e zgjidhjes={stats['solution_depth']}")
    if not trees.graphviz_available():
        print(
            f"Graphviz (programi `dot`) nuk u gjet: në {args.out} u ruajtën vetëm skedarët .dot, "
            f"figurat {args.format} nuk u rigjeneruan. Shih README për instalimin.",
            file=sys.stderr,
        )
        return 1
    print(f"Figurat u ruajtën në {args.out}")
    return 0


def cmd_bench(args: argparse.Namespace) -> int:
    from . import experiments

    experiments.run_all(Path(args.out), img_dir=ROOT / "docs" / "img")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m uninformed_search",
        description="Detyra 1 - Inteligjenca Artificiale: kërkimi i painformuar",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    limit_help = "kufiri i kohës në sekonda (default: %(default)s)"
    landscape_help = "vetëm madhësia e hapësirës së kërkimit (landscape)"

    p = sub.add_parser("golfers", help="Problemi 1: Social Golfers me DFS + backtracking")
    p.add_argument("--groups", "-g", type=_positive, default=8, help="numri i grupeve (default: 8)")
    p.add_argument("--size", "-p", type=_group_size, default=4, help="lojtarë për grup (default: 4)")
    p.add_argument("--weeks", "-w", type=_positive, default=5, help="numri i javëve (default: 5)")
    p.add_argument("--max-weeks", action="store_true", help="provo w = 1, 2, ... derisa DFS të ndalet")
    p.add_argument("--time-limit", type=float, default=60.0, help=limit_help)
    p.add_argument("--landscape", action="store_true", help=landscape_help)
    p.set_defaults(func=cmd_golfers)

    p = sub.add_parser("sudoku", help="Problemi 2: Sudoku me BFS + backtracking")
    p.add_argument(
        "--level", choices=[*sudoku.LEVELS, "all"], default="all", help="niveli i enigmave (default: all)"
    )
    p.add_argument("--puzzle", type=_puzzle, help="enigma si 81 karaktere, 0 ose . për qelizat bosh")
    p.add_argument("--time-limit", type=float, default=60.0, help=limit_help)
    p.add_argument("--landscape", action="store_true", help="shfaq edhe madhësinë e hapësirës së kërkimit")
    p.set_defaults(func=cmd_sudoku)

    p = sub.add_parser("latin", help="Problemi 3: Katrori latin me IDDFS + backtracking")
    p.add_argument("-n", type=_positive, default=5, help="rendi i katrorit (default: 5)")
    p.add_argument("--verbose", "-v", action="store_true", help="shfaq nyjet e çdo iteracioni të IDDFS")
    p.add_argument("--time-limit", type=float, default=60.0, help=limit_help)
    p.add_argument("--landscape", action="store_true", help=landscape_help)
    p.set_defaults(func=cmd_latin)

    p = sub.add_parser("trees", help="Problemi 4: pemët e kërkimit (Graphviz)")
    p.add_argument("--out", default=str(ROOT / "docs" / "img"), help="dosja e figurave (default: docs/img)")
    p.add_argument("--format", choices=["svg", "png", "pdf"], default="svg", help="formati (default: svg)")
    p.add_argument(
        "--ascii",
        choices=[name for name, *_ in trees.FIGURES],
        help="shtyp një pemë në terminal në vend të figurave",
    )
    p.set_defaults(func=cmd_trees)

    p = sub.add_parser("bench", help="ekzekuto të gjitha eksperimentet -> results/ (≈ 3 min)")
    p.add_argument("--out", default=str(ROOT / "results"), help="dosja e tabelave (default: results)")
    p.set_defaults(func=cmd_bench)
    return parser


def main(argv: list[str] | None = None) -> int:
    sys.setrecursionlimit(10_000)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    return args.func(args)
