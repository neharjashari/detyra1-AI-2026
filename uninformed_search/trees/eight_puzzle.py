"""8-Puzzle. State = tiles row by row, 0 is the blank; actions move the blank.

Start and goal are Nilsson's example (283/164/7_5 -> 123/8_4/765).
"""

from __future__ import annotations

from collections import deque

from .core import Problem

MOVES = {"U": -3, "D": 3, "L": -1, "R": 1}
ARROWS = {"U": "↑", "D": "↓", "L": "←", "R": "→"}

NILSSON_START = (2, 8, 3, 1, 6, 4, 7, 0, 5)
NILSSON_GOAL = (1, 2, 3, 8, 0, 4, 7, 6, 5)


class EightPuzzle(Problem):
    def __init__(self, initial=NILSSON_START, goal=NILSSON_GOAL):
        self.initial = tuple(initial)
        self.goal = tuple(goal)
        if sorted(self.initial) != list(range(9)) or sorted(self.goal) != list(range(9)):
            raise ValueError("states must be permutations of 0..8")

    def actions(self, state):
        blank = state.index(0)
        row, col = divmod(blank, 3)
        out = []
        if row > 0:
            out.append("U")
        if row < 2:
            out.append("D")
        if col > 0:
            out.append("L")
        if col < 2:
            out.append("R")
        return out

    def result(self, state, action):
        blank = state.index(0)
        target = blank + MOVES[action]
        cells = list(state)
        cells[blank], cells[target] = cells[target], cells[blank]
        return tuple(cells)

    def is_goal(self, state):
        return state == self.goal

    def action_label(self, action):
        return ARROWS[action]

    def short(self, state):
        return " ".join("".join(str(v) if v else "_" for v in state[r * 3 : r * 3 + 3]) for r in range(3))

    def state_label(self, state):
        rows = []
        for r in range(3):
            cells = []
            for c in range(3):
                v = state[r * 3 + c]
                bg = ' bgcolor="#333333"' if v == 0 else ""
                cells.append(f'<td width="16" height="16"{bg}>{v if v else ""}</td>')
            rows.append("<tr>" + "".join(cells) + "</tr>")
        return (
            '<table border="0" cellborder="1" cellspacing="0" cellpadding="2">' + "".join(rows) + "</table>"
        )


def reachable_states(goal=NILSSON_GOAL) -> dict[int, int]:
    # BFS from the goal over the whole state space, states per distance
    problem = EightPuzzle(goal, goal)
    dist = {problem.goal: 0}
    queue = deque([problem.goal])
    while queue:
        s = queue.popleft()
        for a in problem.actions(s):
            t = problem.result(s, a)
            if t not in dist:
                dist[t] = dist[s] + 1
                queue.append(t)
    layers: dict[int, int] = {}
    for d in dist.values():
        layers[d] = layers.get(d, 0) + 1
    return dict(sorted(layers.items()))
