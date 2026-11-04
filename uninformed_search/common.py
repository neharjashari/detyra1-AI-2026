"""Helpers shared by all problems: search statistics, a time limit, number formatting."""

from __future__ import annotations

import time
from dataclasses import dataclass
from decimal import Decimal


class TimeLimitReached(Exception):
    pass


@dataclass
class SearchStats:
    nodes_generated: int = 0  # children created by the search
    nodes_expanded: int = 0  # nodes whose children were generated
    dead_ends: int = 0  # expanded nodes with no allowed child, the search backtracks from them
    max_frontier: int = 0  # BFS: biggest queue
    max_depth: int = 0  # DFS / IDDFS: deepest node, i.e. the longest path kept in memory
    elapsed: float = 0.0

    def as_dict(self) -> dict:
        return {
            "nodes_generated": self.nodes_generated,
            "nodes_expanded": self.nodes_expanded,
            "dead_ends": self.dead_ends,
            "max_frontier": self.max_frontier,
            "max_depth": self.max_depth,
            "elapsed_s": round(self.elapsed, 3),
        }


class Timer:
    def __init__(self, time_limit: float | None):
        self.time_limit = time_limit
        self.start = time.perf_counter()

    def elapsed(self) -> float:
        return time.perf_counter() - self.start

    def check(self, nodes: int) -> None:
        # looking at the clock costs time, so only do it every 10 000 nodes
        if self.time_limit is not None and nodes % 10_000 == 0 and self.elapsed() > self.time_limit:
            raise TimeLimitReached(f"time limit {self.time_limit}s reached")


def sci(value: int) -> str:
    # 59287247761257140625 -> "5.93e19"; Decimal also works for ints too big for a float
    if value < 10**6:
        return f"{value:,}"
    return f"{Decimal(value):.2e}".replace("e+", "e")
