import pytest

from uninformed_search import social_golfers as golf


def test_upper_bound_for_32_golfers_is_10_weeks():
    assert golf.max_weeks(8, 4) == 10


@pytest.mark.parametrize("g, p, w", [(8, 4, 5), (2, 2, 3), (3, 3, 4), (4, 4, 5)])
def test_dfs_finds_valid_schedule(g, p, w):
    result = golf.solve_dfs(g, p, w)

    assert result.status == "solved"
    assert golf.is_valid(result.schedule, g, p)


def test_dfs_proves_that_2_4_2_has_no_schedule():
    # 8 players, groups of 4: in week 2 every group would need 2 players from the same week-1 group
    result = golf.solve_dfs(2, 4, 2)

    assert result.status == "failure"
    assert result.stats.nodes_generated > 0


def test_more_weeks_than_the_upper_bound_fail_without_search():
    result = golf.solve_dfs(8, 4, 11)

    assert result.status == "failure"
    assert result.stats.nodes_generated == 0


def test_dfs_stops_at_the_time_limit():
    result = golf.solve_dfs(8, 4, 6, time_limit=0.0)

    assert result.status == "limit"


def test_objective_counts_repeated_meetings():
    schedule = [[[0, 1], [2, 3]], [[0, 1], [2, 3]]]  # both pairs meet twice

    assert golf.objective(schedule) == 2
    assert not golf.is_valid(schedule, 2, 2)


def test_week_that_is_not_a_partition_is_invalid():
    schedule = [[[0, 1], [0, 3]]]  # player 0 twice, player 2 missing

    assert not golf.is_valid(schedule, 2, 2)


def test_landscape_for_32_golfers():
    land = golf.landscape(8, 4, 5)

    assert land["partitions_of_one_week"] == 59_287_247_761_257_140_625
    assert land["pairs_of_players"] == 496
    assert land["pairs_per_week"] == 48


def test_max_weeks_dfs_stops_at_the_first_failure():
    results = golf.max_weeks_dfs(2, 4, time_limit=5)

    assert [(w, r.status) for w, r in results] == [(1, "solved"), (2, "failure")]
