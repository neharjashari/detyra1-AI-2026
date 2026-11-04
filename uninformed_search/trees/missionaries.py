"""Missionaries and Cannibals.

State (m, c, b) = missionaries and cannibals on the left bank, b = 1 if the
boat is on the left. Start (3,3,1), goal (0,0,0). M = misionar, K = kanibal.
"""

from __future__ import annotations

from itertools import product

from .core import Problem

LOADS = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]


def load_label(load: tuple[int, int]) -> str:
    m, c = load
    return (f"{m}M" if m else "") + (f"{c}K" if c else "")


class MissionariesCannibals(Problem):
    def __init__(self, people: int = 3, capacity: int = 2):
        self.n = people
        self.capacity = capacity
        self.initial = (people, people, 1)
        self.loads = [
            (m, c) for m in range(capacity + 1) for c in range(capacity + 1) if 1 <= m + c <= capacity
        ]
        self.loads.sort(key=lambda mc: LOADS.index(mc) if mc in LOADS else 99)

    def actions(self, state):
        m, c, b = state
        here_m, here_c = (m, c) if b == 1 else (self.n - m, self.n - c)
        return [(dm, dc) for dm, dc in self.loads if dm <= here_m and dc <= here_c]

    def result(self, state, action):
        m, c, b = state
        dm, dc = action
        return (m - dm, c - dc, 0) if b == 1 else (m + dm, c + dc, 1)

    def is_goal(self, state):
        return state == (0, 0, 0)

    def is_valid(self, state):
        m, c, _ = state
        if not (0 <= m <= self.n and 0 <= c <= self.n):
            return False
        left_ok = m == 0 or m >= c
        right_ok = (self.n - m) == 0 or (self.n - m) >= (self.n - c)
        return left_ok and right_ok

    def action_label(self, action):
        return load_label(action)

    def short(self, state):
        m, c, b = state
        boat = "B" if b else " "
        other = " " if b else "B"
        return f"{m}M{c}K {boat}|~~|{other} {self.n - m}M{self.n - c}K"

    def state_label(self, state):
        m, c, b = state
        left = "M" * m + "<br/>" + "K" * c if m or c else "&nbsp;"
        right = (
            "M" * (self.n - m) + "<br/>" + "K" * (self.n - c) if (self.n - m) or (self.n - c) else "&nbsp;"
        )
        river_l = (
            '<td bgcolor="#9ecae1" width="10">B</td>' if b else '<td bgcolor="#c6dbef" width="10"> </td>'
        )
        river_r = (
            '<td bgcolor="#c6dbef" width="10"> </td>' if b else '<td bgcolor="#9ecae1" width="10">B</td>'
        )
        return (
            '<table border="0" cellborder="0" cellspacing="0" cellpadding="2">'
            f'<tr><td width="34">{left}</td>{river_l}{river_r}<td width="34">{right}</td></tr>'
            f'<tr><td colspan="4"><font point-size="9">({m},{c},{b})</font></td></tr>'
            "</table>"
        )


def state_space(problem: MissionariesCannibals) -> dict:
    # all triples, valid ones, and the ones reachable from the start
    n = problem.n
    all_states = list(product(range(n + 1), range(n + 1), (0, 1)))
    valid = [s for s in all_states if problem.is_valid(s)]
    reachable = {problem.initial}
    stack = [problem.initial]
    while stack:
        s = stack.pop()
        for a in problem.actions(s):
            t = problem.result(s, a)
            if problem.is_valid(t) and t not in reachable:
                reachable.add(t)
                stack.append(t)
    return {"all": len(all_states), "valid": len(valid), "reachable": len(reachable)}
