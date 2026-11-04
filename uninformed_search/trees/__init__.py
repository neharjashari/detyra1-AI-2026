"""Problem 4: search trees for 8-Puzzle, Missionaries & Cannibals and RWS."""

from __future__ import annotations

from pathlib import Path

from .core import SearchTree, ascii_tree, build_tree, graphviz_available, render, to_dot
from .eight_puzzle import EightPuzzle
from .missionaries import MissionariesCannibals
from .rotating_workforce import RotatingWorkforce

# name, problem, build_tree options, title, graph direction
FIGURES = [
    (
        "8puzzle_full_depth3",
        EightPuzzle,
        {"strategy": "bfs", "max_depth": 3, "repeated": "none", "stop_at_goal": False},
        "8-Puzzle: pema e plotë e kërkimit deri në thellësinë 3 (pa eliminim të gjendjeve të përsëritura)",
        "TB",
    ),
    (
        "8puzzle_bfs_graph",
        EightPuzzle,
        {"strategy": "bfs", "repeated": "explored"},
        "8-Puzzle: pema e BFS (graph search) deri te qëllimi",
        "TB",
    ),
    (
        "mc_bfs_graph",
        MissionariesCannibals,
        {"strategy": "bfs", "repeated": "explored"},
        "Misionarët dhe Kanibalët: pema e BFS (graph search) deri te qëllimi",
        "TB",
    ),
    (
        "mc_dfs_ancestors",
        MissionariesCannibals,
        {"strategy": "dfs", "repeated": "ancestors"},
        "Misionarët dhe Kanibalët: pema e DFS (pa cikle në shteg) deri te qëllimi",
        "TB",
    ),
    (
        "rws_full_depth2",
        RotatingWorkforce,
        {"strategy": "bfs", "max_depth": 2, "repeated": "none", "stop_at_goal": False},
        "Rotating Workforce: pema e plotë deri në thellësinë 2 (dita e hënë dhe e martë)",
        "TB",
    ),
    (
        "rws_dfs",
        RotatingWorkforce,
        {"strategy": "dfs", "repeated": "none"},
        "Rotating Workforce: pema e DFS me backtracking deri te orari i parë i vlefshëm",
        "LR",
    ),
]


def build_figure(name: str) -> tuple[SearchTree, str, str]:
    for fig_name, factory, kwargs, title, rankdir in FIGURES:
        if fig_name == name:
            return build_tree(factory(), **kwargs), title, rankdir
    raise KeyError(name)


def render_all(out_dir: Path, fmt: str = "svg") -> dict[str, dict]:
    out_dir = Path(out_dir)
    summary = {}
    for name, *_ in FIGURES:
        tree, title, rankdir = build_figure(name)
        render(to_dot(tree, title, rankdir=rankdir), out_dir / name, fmt)
        summary[name] = tree.stats()
    return summary


__all__ = [
    "FIGURES",
    "EightPuzzle",
    "MissionariesCannibals",
    "RotatingWorkforce",
    "ascii_tree",
    "build_figure",
    "build_tree",
    "graphviz_available",
    "render_all",
    "to_dot",
]
