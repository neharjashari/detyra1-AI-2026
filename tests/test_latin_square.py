import itertools

import pytest

from uninformed_search import latin_square as latin


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_iddfs_returns_latin_square(n):
    result = latin.solve_iddfs(n)

    assert result.status == "solved"
    assert latin.is_latin_square(result.square)


def test_iddfs_needs_one_iteration_per_depth_up_to_n_squared():
    result = latin.solve_iddfs(4)

    assert [it.limit for it in result.iterations] == list(range(17))
    assert [it.result for it in result.iterations] == ["cutoff"] * 16 + ["solved"]


def test_iddfs_stops_at_the_time_limit():
    result = latin.solve_iddfs(7, time_limit=0.0)

    assert result.status == "limit"


@pytest.mark.parametrize("n", [1, 2, 3, 4])
def test_known_counts_match_a_brute_force_count(n):
    # every row is a permutation; keep the combinations whose columns have no repeated value
    rows = list(itertools.permutations(range(1, n + 1)))
    count = sum(
        1
        for square in itertools.product(rows, repeat=n)
        if all(len(set(column)) == n for column in zip(*square))
    )

    assert count == latin.KNOWN_COUNTS[n]


def test_objective_counts_repeated_values():
    square = [[1, 2], [1, 2]]  # both columns repeat a value

    assert latin.objective(square) == 2
    assert not latin.is_latin_square(square)


def test_landscape_for_order_5():
    land = latin.landscape(5)

    assert land["any_value_in_every_cell"] == 5**25
    assert land["every_row_a_permutation"] == 120**5
    assert land["latin_squares"] == 161_280
