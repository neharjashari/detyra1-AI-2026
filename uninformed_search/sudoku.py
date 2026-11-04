"""Problem 2: Sudoku with BFS and backtracking.

A grid is a string of 81 characters read row by row; "." is an empty cell.
The model is explained in docs/02-sudoku.md.
"""

from __future__ import annotations

import math
from collections import deque
from dataclasses import dataclass
from pathlib import Path

from .common import SearchStats, TimeLimitReached, Timer

DIGITS = "123456789"
LEVELS = ("easy", "medium", "hard")
DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "sudoku"


@dataclass
class SudokuResult:
    status: str  # solved / failure / limit
    solution: str | None
    stats: SearchStats
    reason: str = ""


# reading and printing


def parse(text: str) -> str:
    # digits, "." or "0" for an empty cell; everything else (spaces, |, -) is ignored
    cells = [ch for ch in text if ch in "0123456789."]
    if len(cells) != 81:
        raise ValueError(f"a Sudoku needs 81 cells, got {len(cells)}")
    return "".join(cells).replace("0", ".")


def load_puzzles(level: str) -> list[tuple[str, str]]:
    # one puzzle per line as "name: <81 characters>"; lines starting with # are comments
    puzzles = []
    for line in (DATA_DIR / f"{level}.txt").read_text(encoding="utf-8").splitlines():
        if line.strip() and not line.startswith("#"):
            name, cells = line.split(":", 1)
            puzzles.append((name.strip(), parse(cells)))
    return puzzles


def level_of(puzzle: str) -> str:
    # fewer givens = more empty cells = a deeper and wider search tree
    givens = 81 - puzzle.count(".")
    if givens >= 30:
        return "easy"
    if givens >= 26:
        return "medium"
    return "hard"


def format_grid(grid: str) -> str:
    lines = []
    for r in range(9):
        if r in (3, 6):
            lines.append("------+-------+------")
        row = grid[r * 9 : r * 9 + 9]
        lines.append(" | ".join(" ".join(row[c : c + 3]) for c in (0, 3, 6)))
    return "\n".join(lines)


# rows, columns, boxes and the constraints


def row_of(grid: str, r: int) -> str:
    return grid[r * 9 : r * 9 + 9]


def column_of(grid: str, c: int) -> str:
    return grid[c::9]


def box_of(grid: str, r: int, c: int) -> str:
    top, left = r // 3 * 3, c // 3 * 3
    return "".join(grid[(top + i) * 9 + left : (top + i) * 9 + left + 3] for i in range(3))


def units(grid: str) -> list[str]:
    # the 27 groups that must contain 1..9 once: 9 rows, 9 columns, 9 boxes
    rows = [row_of(grid, r) for r in range(9)]
    columns = [column_of(grid, c) for c in range(9)]
    boxes = [box_of(grid, r, c) for r in (0, 3, 6) for c in (0, 3, 6)]
    return rows + columns + boxes


def allowed_digits(grid: str, cell: int) -> list[str]:
    r, c = divmod(cell, 9)
    used = set(row_of(grid, r) + column_of(grid, c) + box_of(grid, r, c))
    return [d for d in DIGITS if d not in used]


def has_conflicts(grid: str) -> bool:
    # the same digit twice in a row, column or box
    for unit in units(grid):
        digits = unit.replace(".", "")
        if len(digits) != len(set(digits)):
            return True
    return False


def objective(grid: str) -> int:
    """f = sum over the 27 units of (9 - distinct digits); 0 only for a solved grid."""
    return sum(9 - len(set(unit.replace(".", ""))) for unit in units(grid))


def is_solution(grid: str, puzzle: str) -> bool:
    keeps_givens = all(p in (".", g) for p, g in zip(puzzle, grid, strict=True))
    return "." not in grid and objective(grid) == 0 and keeps_givens


# landscape


def landscape(puzzle: str) -> dict:
    empty = puzzle.count(".")
    every_row_a_permutation = 1
    for r in range(9):
        every_row_a_permutation *= math.factorial(row_of(puzzle, r).count("."))
    return {
        "givens": 81 - empty,
        "empty_cells": empty,
        "any_digit_in_every_empty_cell": 9**empty,
        "every_row_a_permutation": every_row_a_permutation,
    }


# BFS with backtracking


def solve_bfs(puzzle: str, time_limit: float | None = None, frontier_limit: int = 2_000_000) -> SudokuResult:
    """BFS over partially filled grids.

    Action = write a digit in the first empty cell. Only digits that break no
    rule are generated (backtracking), so a grid whose first empty cell has no
    allowed digit is a dead end and its branch is dropped. The goal test is done
    when a child is generated, as in AIMA. BFS keeps whole levels of the tree in
    the queue, so the search also stops when the queue gets too big for the memory.
    """
    if has_conflicts(puzzle):
        raise ValueError("the givens break the Sudoku rules")
    stats = SearchStats()
    timer = Timer(time_limit)

    def finish(status: str, solution: str | None = None, reason: str = "") -> SudokuResult:
        stats.elapsed = timer.elapsed()
        return SudokuResult(status, solution, stats, reason)

    if "." not in puzzle:
        return finish("solved", puzzle)
    frontier = deque([puzzle])  # FIFO queue
    try:
        while frontier:
            grid = frontier.popleft()
            stats.nodes_expanded += 1
            cell = grid.index(".")
            digits = allowed_digits(grid, cell)
            if not digits:
                stats.dead_ends += 1
            for digit in digits:
                child = grid[:cell] + digit + grid[cell + 1 :]
                stats.nodes_generated += 1
                timer.check(stats.nodes_generated)
                if "." not in child:
                    return finish("solved", child)
                frontier.append(child)
            stats.max_frontier = max(stats.max_frontier, len(frontier))
            if len(frontier) > frontier_limit:
                return finish("limit", reason=f"frontier limit {frontier_limit} reached")
    except TimeLimitReached as exc:
        return finish("limit", reason=str(exc))
    return finish("failure", reason="the whole search tree was explored")
