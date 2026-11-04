"""Problem 3: Latin square of order n with IDDFS and backtracking.

Cells are filled row by row. A value is placed only if it is not used yet in
its row or column. Every solution is at depth n * n (all cells filled).
The model is explained in docs/03-latin-square.md.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from .common import SearchStats, TimeLimitReached, Timer

# number of Latin squares of order n, OEIS A002860 (https://oeis.org/A002860)
KNOWN_COUNTS = {1: 1, 2: 2, 3: 12, 4: 576, 5: 161_280, 6: 812_851_200, 7: 61_479_419_904_000}

SOLVED, CUTOFF, FAILURE = "solved", "cutoff", "failure"


def objective(square: list[list[int]]) -> int:
    """f = sum over rows and columns of (n - distinct values); 0 only for a Latin square."""
    n = len(square)
    rows = sum(n - len(set(row)) for row in square)
    columns = sum(n - len({square[r][c] for r in range(n)}) for c in range(n))
    return rows + columns


def is_latin_square(square: list[list[int]]) -> bool:
    n = len(square)
    in_range = all(len(row) == n and all(1 <= v <= n for v in row) for row in square)
    return in_range and objective(square) == 0


def format_square(square: list[list[int]]) -> str:
    width = len(str(len(square)))
    return "\n".join(" ".join(str(v).rjust(width) for v in row) for row in square)


def landscape(n: int) -> dict:
    return {
        "cells": n * n,
        "any_value_in_every_cell": n ** (n * n),
        "every_row_a_permutation": math.factorial(n) ** n,
        "latin_squares": KNOWN_COUNTS.get(n),
    }


@dataclass
class Iteration:
    limit: int
    nodes: int  # nodes generated in this iteration
    result: str


@dataclass
class LatinResult:
    status: str  # solved / failure / limit
    square: list[list[int]] | None
    stats: SearchStats
    iterations: list[Iteration] = field(default_factory=list)
    reason: str = ""


def solve_iddfs(n: int, time_limit: float | None = None) -> LatinResult:
    """IDDFS: depth-limited DFS with limit 0, 1, 2, ... until a solution is found.

    Inside each iteration the DFS backtracks: a value is tried in a cell only if
    it is not in the same row or column, and the move is undone when the branch fails.
    """
    if n < 1:
        raise ValueError("n must be positive")
    square = [[0] * n for _ in range(n)]
    in_row = [set() for _ in range(n)]  # values already used in each row
    in_column = [set() for _ in range(n)]
    stats = SearchStats()
    timer = Timer(time_limit)
    iterations: list[Iteration] = []

    def depth_limited(depth: int, limit: int) -> str:
        if depth == n * n:
            return SOLVED  # goal: every cell is filled
        if depth == limit:
            return CUTOFF  # the node may have children below the limit
        r, c = divmod(depth, n)
        stats.nodes_expanded += 1
        allowed = [v for v in range(1, n + 1) if v not in in_row[r] and v not in in_column[c]]
        if not allowed:
            stats.dead_ends += 1
        cutoff = False
        for value in allowed:
            stats.nodes_generated += 1
            timer.check(stats.nodes_generated)
            square[r][c] = value
            in_row[r].add(value)
            in_column[c].add(value)
            result = depth_limited(depth + 1, limit)
            if result == SOLVED:
                return SOLVED
            # backtrack: undo the move and try the next value
            square[r][c] = 0
            in_row[r].remove(value)
            in_column[c].remove(value)
            if result == CUTOFF:
                cutoff = True
        return CUTOFF if cutoff else FAILURE

    status, reason = FAILURE, ""
    try:
        for limit in range(n * n + 1):
            before = stats.nodes_generated
            result = depth_limited(0, limit)
            iterations.append(Iteration(limit, stats.nodes_generated - before, result))
            stats.max_depth = limit
            if result == SOLVED:
                status = SOLVED
                break
            if result == FAILURE:
                reason = "no cutoff: the whole search tree was explored"
                break
    except TimeLimitReached as exc:
        status, reason = "limit", str(exc)
    stats.elapsed = timer.elapsed()
    return LatinResult(status, square if status == SOLVED else None, stats, iterations, reason)
