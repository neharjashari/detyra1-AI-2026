"""Problem 1: Social Golfers with DFS and backtracking.

n = g * p golfers play every week in g groups of p players. Two golfers may
share a group at most once. The model is explained in docs/01-social-golfers.md.
"""

from __future__ import annotations

import itertools
import math
from dataclasses import dataclass

from .common import SearchStats, TimeLimitReached, Timer

Schedule = list[list[list[int]]]  # schedule[week][group] = players of that group


@dataclass
class GolfResult:
    status: str  # solved / failure / limit
    schedule: Schedule | None
    stats: SearchStats
    reason: str = ""


def max_weeks(groups: int, size: int) -> int:
    # every week a player meets size - 1 new players, and there are only n - 1 others
    return (groups * size - 1) // (size - 1)


def objective(schedule: Schedule) -> int:
    """f = number of repeated meetings: sum over all pairs of max(0, meetings - 1)."""
    meetings: dict[tuple[int, int], int] = {}
    for week in schedule:
        for group in week:
            for pair in itertools.combinations(sorted(group), 2):
                meetings[pair] = meetings.get(pair, 0) + 1
    return sum(count - 1 for count in meetings.values() if count > 1)


def is_valid(schedule: Schedule, groups: int, size: int) -> bool:
    everyone = list(range(groups * size))
    for week in schedule:
        if len(week) != groups or any(len(group) != size for group in week):
            return False
        if sorted(player for group in week for player in group) != everyone:
            return False  # somebody plays twice or not at all in this week
    return objective(schedule) == 0


def landscape(groups: int, size: int, weeks: int) -> dict:
    n = groups * size
    # ways to split n players into g groups of p (order of groups and inside groups ignored)
    partitions = math.factorial(n) // (math.factorial(size) ** groups * math.factorial(groups))
    return {
        "every_slot_any_player": n ** (n * weeks),
        "every_week_a_permutation": math.factorial(n) ** weeks,
        "every_week_a_partition": partitions**weeks,
        "partitions_of_one_week": partitions,
        "pairs_of_players": n * (n - 1) // 2,
        "pairs_per_week": groups * size * (size - 1) // 2,
        "upper_bound_weeks": max_weeks(groups, size),
    }


def solve_dfs(groups: int, size: int, weeks: int, time_limit: float | None = None) -> GolfResult:
    """DFS with backtracking that fills the schedule one slot at a time.

    Slots are filled week by week, group by group. A player is allowed in a slot
    only if that player does not play yet in that week and has not met anybody in
    the group. Players inside a group are increasing and every group starts with
    the smallest free player, so the same week is never built twice in another order.
    """
    n = groups * size
    stats = SearchStats()
    if weeks > max_weeks(groups, size):
        return GolfResult("failure", None, stats, "w is larger than the upper bound")

    schedule: Schedule = [[[] for _ in range(groups)] for _ in range(weeks)]
    playing = [set() for _ in range(weeks)]  # players already placed in each week
    met = [set() for _ in range(n)]  # met[a] = players that a has already played with
    timer = Timer(time_limit)

    def allowed_players(week: int, group: list[int]) -> list[int]:
        if not group:
            return [min(p for p in range(n) if p not in playing[week])]
        return [p for p in range(group[-1] + 1, n) if p not in playing[week] and met[p].isdisjoint(group)]

    def dfs(slot: int) -> bool:
        if slot == weeks * n:
            return True  # goal: every slot is filled
        week, position = divmod(slot, n)
        group = schedule[week][position // size]
        stats.nodes_expanded += 1
        stats.max_depth = max(stats.max_depth, slot)
        candidates = allowed_players(week, group)
        if not candidates:
            stats.dead_ends += 1
        for player in candidates:
            stats.nodes_generated += 1
            timer.check(stats.nodes_generated)
            for other in group:
                met[player].add(other)
                met[other].add(player)
            group.append(player)
            playing[week].add(player)
            if dfs(slot + 1):
                return True
            # backtrack: undo the move and try the next player
            group.pop()
            playing[week].remove(player)
            for other in group:
                met[player].remove(other)
                met[other].remove(player)
        return False

    try:
        found = dfs(0)
    except TimeLimitReached as exc:
        stats.elapsed = timer.elapsed()
        return GolfResult("limit", None, stats, str(exc))
    stats.elapsed = timer.elapsed()
    if found:
        return GolfResult("solved", schedule, stats)
    return GolfResult("failure", None, stats, "the whole search tree was explored")


def max_weeks_dfs(groups: int, size: int, time_limit: float | None = 60.0) -> list[tuple[int, GolfResult]]:
    """Run the DFS for w = 1, 2, ... until it fails or reaches the time limit."""
    results = []
    for weeks in range(1, max_weeks(groups, size) + 1):
        result = solve_dfs(groups, size, weeks, time_limit)
        results.append((weeks, result))
        if result.status != "solved":
            break
    return results


def format_schedule(schedule: Schedule) -> str:
    width = max(len(str(p)) for week in schedule for group in week for p in group)
    lines = []
    for number, week in enumerate(schedule, start=1):
        groups = "  |  ".join(" ".join(str(p).rjust(width) for p in group) for group in week)
        lines.append(f"Java {number:>2}:  {groups}")
    return "\n".join(lines)
