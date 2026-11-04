"""Rotating Workforce Scheduling on a small instance (3 employees, one week).

Row i of the 3x7 matrix is employee i's week; the rows are read one after
another as one cyclic sequence. The tree is built day by day: each action
fills one column with an arrangement of that day's demand (1 D, 1 N, 1 free).
Constraints of the instance are in RWSInstance; see docs/04-search-trees.md.
"""

from __future__ import annotations

from dataclasses import dataclass
from itertools import permutations

from .core import Problem

OFF = "-"
DAYS = ("Hë", "Ma", "Më", "En", "Pr", "Sh", "Di")
COLORS = {"D": "#ffe08a", "N": "#8fb3e8", OFF: "#ffffff"}


@dataclass(frozen=True)
class RWSInstance:
    employees: int = 3
    shifts: tuple[str, ...] = ("D", "N")
    requirements: tuple[tuple[int, ...], ...] = ((1,) * 7, (1,) * 7)  # [shift][day]
    work_block: tuple[int, int] = (2, 4)
    off_block: tuple[int, int] = (1, 2)
    shift_block: tuple[tuple[int, int], ...] = ((1, 3), (2, 3))  # [shift]
    forbidden: tuple[tuple[str, str], ...] = (("N", "D"),)
    days: int = 7

    def demand(self, day: int) -> str:
        # symbols needed on this day, e.g. "DN-"
        work = "".join(s * self.requirements[k][day] for k, s in enumerate(self.shifts))
        if len(work) > self.employees:
            raise ValueError(f"day {day} needs more than {self.employees} employees")
        return work + OFF * (self.employees - len(work))


def _runs(seq: str, key, cyclic: bool) -> list[tuple[str, int, bool]]:
    # blocks of equal key(symbol) as (class, length, closed on both sides)
    if not seq:
        return []
    classes = [key(ch) for ch in seq]
    if cyclic:
        if len(set(classes)) == 1:
            return [(classes[0], 10**9, True)]  # one endless block
        start = next(i for i in range(len(classes)) if classes[i] != classes[i - 1])
        classes = classes[start:] + classes[:start]
    runs, i = [], 0
    while i < len(classes):
        j = i
        while j < len(classes) and classes[j] == classes[i]:
            j += 1
        closed = cyclic or (i > 0 and j < len(classes))
        runs.append((classes[i], j - i, closed))
        i = j
    return runs


def check(seq: str, inst: RWSInstance, cyclic: bool) -> list[str]:
    # list of broken constraints; a block touching the end of a partial row is still open
    problems: list[str] = []
    pairs = [(seq[i], seq[i + 1]) for i in range(len(seq) - 1)]
    if cyclic and seq:
        pairs.append((seq[-1], seq[0]))
    for a, b in pairs:
        if (a, b) in inst.forbidden:
            problems.append(f"forbidden {a}->{b}")

    def bounds_for(kind: str, cls: str) -> tuple[int, int] | None:
        if kind == "work":
            return inst.work_block if cls == "W" else inst.off_block
        if cls == OFF:
            return None
        return inst.shift_block[inst.shifts.index(cls)]

    for kind, key in (("work", lambda ch: OFF if ch == OFF else "W"), ("shift", lambda ch: ch)):
        for cls, length, closed in _runs(seq, key, cyclic):
            limits = bounds_for(kind, cls)
            if limits is None:
                continue
            low, high = limits
            if length > high:
                problems.append(f"{kind} block '{cls}' longer than {high}")
            if closed and length < low:
                problems.append(f"{kind} block '{cls}' shorter than {low}")
    return problems


class RotatingWorkforce(Problem):
    def __init__(self, inst: RWSInstance | None = None):
        self.inst = inst or RWSInstance()
        self.initial: tuple[str, ...] = ()

    # state = tuple of columns (one string per day, one char per employee)
    def rows(self, state) -> list[str]:
        return ["".join(col[e] for col in state) for e in range(self.inst.employees)]

    def actions(self, state):
        if len(state) >= self.inst.days:
            return []
        demand = self.inst.demand(len(state))
        return sorted({"".join(p) for p in permutations(demand)})

    def result(self, state, action):
        return state + (action,)

    def is_valid(self, state):
        if len(state) == self.inst.days:
            return not check("".join(self.rows(state)), self.inst, cyclic=True)
        return all(not check(row, self.inst, cyclic=False) for row in self.rows(state))

    def is_goal(self, state):
        return len(state) == self.inst.days and self.is_valid(state)

    def action_label(self, action):
        return action

    def short(self, state):
        return "/".join(self.rows(state)) if state else "(bosh)"

    def state_label(self, state):
        if not state:
            return "<i>orari bosh</i>"
        rows = []
        for row in self.rows(state):
            cells = "".join(
                f'<td bgcolor="{COLORS[ch]}" width="13">{ch if ch != OFF else "&#8211;"}</td>' for ch in row
            )
            rows.append(f"<tr>{cells}</tr>")
        header = "".join(f'<td><font point-size="8">{DAYS[d]}</font></td>' for d in range(len(state)))
        return (
            '<table border="0" cellborder="1" cellspacing="0" cellpadding="1">'
            f"<tr>{header}</tr>{''.join(rows)}</table>"
        )


def format_schedule(problem: RotatingWorkforce, state) -> str:
    lines = ["Pun.  " + "  ".join(DAYS)]
    for e, row in enumerate(problem.rows(state), start=1):
        lines.append(f"  {e}   " + "   ".join(row))
    return "\n".join(lines)


def search_space(problem: RotatingWorkforce) -> dict:
    inst = problem.inst
    per_day = [len({"".join(p) for p in permutations(inst.demand(d))}) for d in range(inst.days)]
    leaves = 1
    for count in per_day:
        leaves *= count
    symbols = len(inst.shifts) + 1
    return {
        "actions_per_level": per_day,
        "leaves_column_wise": leaves,
        "cell_wise": symbols ** (inst.employees * inst.days),
    }
