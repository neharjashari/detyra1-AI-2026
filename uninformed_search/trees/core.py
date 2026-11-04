"""Builds search trees (BFS or DFS) and exports them to Graphviz.

Every generated node is kept, including invalid and repeated ones, so the
picture shows exactly what the search did.
"""

from __future__ import annotations

import html
import shutil
import subprocess
from collections import Counter, deque
from collections.abc import Hashable, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


class Problem:
    initial: Hashable

    def actions(self, state: Hashable) -> Iterable[Any]:
        raise NotImplementedError

    def result(self, state: Hashable, action: Any) -> Hashable:
        raise NotImplementedError

    def is_goal(self, state: Hashable) -> bool:
        raise NotImplementedError

    def is_valid(self, state: Hashable) -> bool:
        # invalid states are drawn but not expanded
        return True

    def action_label(self, action: Any) -> str:
        return str(action)

    def state_label(self, state: Hashable) -> str:
        # graphviz HTML label, without the outer < >
        return html.escape(self.short(state))

    def short(self, state: Hashable) -> str:
        return str(state)


NORMAL, GOAL, INVALID, REPEATED, UNEXPANDED = "normal", "goal", "invalid", "repeated", "unexpanded"


@dataclass
class Node:
    id: int
    state: Hashable
    parent: Node | None
    action: Any
    depth: int
    status: str = NORMAL
    children: list[Node] = field(default_factory=list)
    order: int | None = None  # when it was expanded (1, 2, ...)
    duplicate: bool = False  # same state as an ancestor (only marked when repeated="none")

    def path(self) -> list[Node]:
        node, out = self, []
        while node is not None:
            out.append(node)
            node = node.parent
        return out[::-1]

    def ancestors_states(self) -> set:
        return {n.state for n in self.path()[:-1]}


@dataclass
class SearchTree:
    problem: Problem
    root: Node
    nodes: list[Node]
    goal: Node | None
    strategy: str
    repeated: str
    max_depth: int | None

    def solution_ids(self) -> set[int]:
        return {n.id for n in self.goal.path()} if self.goal else set()

    def stats(self) -> dict:
        per_depth = Counter(n.depth for n in self.nodes)
        status = Counter(n.status for n in self.nodes)
        expanded = [n for n in self.nodes if n.order is not None]
        children = sum(len(n.children) for n in expanded)
        return {
            "nodes": len(self.nodes),
            "expanded": len(expanded),
            "per_depth": [per_depth[d] for d in range(max(per_depth) + 1)],
            "status": dict(status),
            "avg_branching": round(children / len(expanded), 2) if expanded else 0,
            "solution_depth": self.goal.depth if self.goal else None,
            "solution": [self.problem.action_label(n.action) for n in self.goal.path()[1:]]
            if self.goal
            else None,
        }


def build_tree(
    problem: Problem,
    strategy: str = "bfs",
    max_depth: int | None = None,
    repeated: str = "explored",
    stop_at_goal: bool = True,
    max_nodes: int = 2000,
) -> SearchTree:
    """repeated: "none" (tree search), "ancestors" (skip states already on the
    path) or "explored" (graph search). The goal test is done on generation."""
    if strategy not in ("bfs", "dfs"):
        raise ValueError("strategy must be 'bfs' or 'dfs'")
    if repeated not in ("none", "ancestors", "explored"):
        raise ValueError("repeated must be 'none', 'ancestors' or 'explored'")

    root = Node(0, problem.initial, None, None, 0)
    nodes = [root]
    seen = {root.state}
    goal: Node | None = None
    expansions = 0
    if problem.is_goal(root.state):
        root.status = GOAL
        return SearchTree(problem, root, nodes, root, strategy, repeated, max_depth)

    def generate(parent: Node, action: Any) -> Node:
        nonlocal goal
        state = problem.result(parent.state, action)
        child = Node(len(nodes), state, parent, action, parent.depth + 1)
        nodes.append(child)
        parent.children.append(child)
        if not problem.is_valid(state):
            child.status = INVALID
        elif (
            repeated == "explored"
            and state in seen
            or repeated == "ancestors"
            and state in parent.ancestors_states() | {parent.state}
        ):
            child.status = REPEATED
        elif problem.is_goal(state):
            child.status = GOAL
            goal = goal or child
        if repeated == "none" and state in parent.ancestors_states() | {parent.state}:
            child.duplicate = True
        seen.add(state)
        return child

    def expandable(node: Node) -> bool:
        if node.status != NORMAL:
            return False
        if max_depth is not None and node.depth >= max_depth:
            node.status = UNEXPANDED
            return False
        return True

    if strategy == "bfs":
        frontier = deque([root])
        while frontier and len(nodes) < max_nodes:
            node = frontier.popleft()
            if not expandable(node):
                continue
            expansions += 1
            node.order = expansions
            for action in problem.actions(node.state):
                child = generate(node, action)
                if child.status == NORMAL:
                    frontier.append(child)
                if goal and stop_at_goal:
                    break
            if goal and stop_at_goal:
                break
        for node in frontier:
            if node.status == NORMAL:
                node.status = UNEXPANDED
    else:

        def dfs(node: Node) -> bool:
            nonlocal expansions
            if not expandable(node) or len(nodes) >= max_nodes:
                return False
            expansions += 1
            node.order = expansions
            for action in problem.actions(node.state):
                child = generate(node, action)
                if goal and stop_at_goal:
                    return True
                if child.status == NORMAL and dfs(child):
                    return True
            return False

        dfs(root)

    return SearchTree(problem, root, nodes, goal, strategy, repeated, max_depth)


# Graphviz export

STYLE = {
    NORMAL: 'fillcolor="#ffffff"',
    GOAL: 'fillcolor="#b7e4c7" penwidth=2.5 color="#1b7f3b"',
    INVALID: 'fillcolor="#f8c9c4" color="#c0392b"',
    REPEATED: 'fillcolor="#e5e5e5" color="#8a8a8a" style="filled,dashed"',
    UNEXPANDED: 'fillcolor="#ffffff" color="#8a8a8a" style="filled,dotted"',
}
LEGEND = {
    NORMAL: "nyje e zgjeruar",
    GOAL: "gjendje qëllim",
    INVALID: "gjendje e palejuar (shkel kufizimet)",
    REPEATED: "gjendje e përsëritur (nuk zgjerohet)",
    UNEXPANDED: "nyje e pazgjeruar (kufiri i thellësisë / frontier)",
}


def to_dot(tree: SearchTree, title: str, rankdir: str = "TB", show_order: bool = True) -> str:
    on_path = tree.solution_ids()
    used = {n.status for n in tree.nodes}
    lines = [
        "digraph SearchTree {",
        (
            f'  graph [rankdir={rankdir} labelloc="t" fontsize=20 fontname="Helvetica" '
            f"label=<<b>{html.escape(title)}</b>> nodesep=0.15 ranksep=0.45];"
        ),
        '  node [shape=box style=filled fontname="Helvetica" fontsize=11 margin="0.04,0.03"];',
        '  edge [fontname="Helvetica" fontsize=10 color="#555555" arrowsize=0.6];',
    ]
    for node in tree.nodes:
        label = tree.problem.state_label(node.state)
        caption = []
        if show_order and node.order is not None:
            caption.append(f"#{node.order}")
        caption.append(f"d={node.depth}")
        label = (
            f'<table border="0" cellborder="0" cellspacing="0" cellpadding="0">'
            f"<tr><td>{label}</td></tr>"
            f'<tr><td><font point-size="9" color="#666666">{" ".join(caption)}</font></td></tr>'
            f"</table>"
        )
        style = STYLE[node.status]
        if node.id in on_path and node.status != GOAL:
            style = 'fillcolor="#e3f4ea" color="#1b7f3b" penwidth=2'
        if node.duplicate:
            style += ' color="#e67e22" penwidth=2.5'
        lines.append(f"  n{node.id} [label=<{label}> {style}];")
    for node in tree.nodes:
        for child in node.children:
            attrs = f'label="{html.escape(tree.problem.action_label(child.action))}"'
            if child.id in on_path:
                attrs += ' color="#1b7f3b" penwidth=2.2 fontcolor="#1b7f3b"'
            lines.append(f"  n{node.id} -> n{child.id} [{attrs}];")
    # legend as a single html table node
    swatches = {
        NORMAL: ("#ffffff", "#333333"),
        GOAL: ("#b7e4c7", "#1b7f3b"),
        INVALID: ("#f8c9c4", "#c0392b"),
        REPEATED: ("#e5e5e5", "#8a8a8a"),
        UNEXPANDED: ("#ffffff", "#bbbbbb"),
    }
    rows = ['<tr><td colspan="2"><b>Legjenda</b></td></tr>']
    for status in (NORMAL, GOAL, INVALID, REPEATED, UNEXPANDED):
        if status in used:
            fill, border = swatches[status]
            rows.append(
                f'<tr><td width="18" height="12" bgcolor="{fill}" color="{border}" border="1"></td>'
                f'<td align="left">{LEGEND[status]}</td></tr>'
            )
    if any(n.duplicate for n in tree.nodes):
        rows.append(
            '<tr><td width="18" height="12" bgcolor="#ffffff" color="#e67e22" border="2"></td>'
            '<td align="left">gjendje e njëjtë me një paraardhës '
            "(pemë pa kontroll, zgjerohet sërish)</td></tr>"
        )
    if on_path:
        rows.append(
            '<tr><td width="18" height="12" bgcolor="#e3f4ea" color="#1b7f3b" border="2"></td>'
            '<td align="left">shtegu i zgjidhjes (veprimet me të gjelbër)</td></tr>'
        )
    lines.append(
        '  legend [shape=plaintext style="" fontsize=10 label=<'
        '<table border="1" color="#bbbbbb" cellborder="0" cellspacing="3" cellpadding="2">'
        + "".join(rows)
        + "</table>>];"
    )
    lines.append("}")
    return "\n".join(lines)


def graphviz_available() -> bool:
    return shutil.which("dot") is not None


def render(dot: str, path: Path, fmt: str = "svg") -> Path | None:
    # always writes the .dot file, the image only if graphviz is installed
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    dot_path = path.with_suffix(".dot")
    dot_path.write_text(dot, encoding="utf-8")
    if not graphviz_available():
        return None
    out = path.with_suffix(f".{fmt}")
    subprocess.run(["dot", f"-T{fmt}", str(dot_path), "-o", str(out)], check=True)
    return out


def ascii_tree(tree: SearchTree, max_lines: int = 200) -> str:
    lines: list[str] = []
    marks = {GOAL: " [QËLLIM]", INVALID: " [i palejuar]", REPEATED: " [përsëritur]", UNEXPANDED: " [...]"}

    def walk(node: Node, prefix: str, last: bool) -> None:
        if len(lines) >= max_lines:
            return
        connector = "" if node.parent is None else ("└── " if last else "├── ")
        action = "" if node.action is None else f"{tree.problem.action_label(node.action)}: "
        lines.append(
            f"{prefix}{connector}{action}{tree.problem.short(node.state)}{marks.get(node.status, '')}"
        )
        child_prefix = prefix + ("" if node.parent is None else ("    " if last else "│   "))
        for i, child in enumerate(node.children):
            walk(child, child_prefix, i == len(node.children) - 1)

    walk(tree.root, "", True)
    if len(lines) >= max_lines:
        lines.append("...")
    return "\n".join(lines)
