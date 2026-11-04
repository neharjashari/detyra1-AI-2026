from uninformed_search.trees import build_figure, to_dot
from uninformed_search.trees.core import build_tree
from uninformed_search.trees.eight_puzzle import EightPuzzle, reachable_states
from uninformed_search.trees.missionaries import MissionariesCannibals, state_space
from uninformed_search.trees.rotating_workforce import RotatingWorkforce, check


def test_eight_puzzle_bfs_finds_shortest_solution():
    tree = build_tree(EightPuzzle(), "bfs", repeated="explored")
    assert tree.goal is not None and tree.goal.depth == 5


def test_eight_puzzle_has_181440_reachable_states():
    assert sum(reachable_states().values()) == 181440


def test_missionaries_shortest_solution_has_11_crossings():
    tree = build_tree(MissionariesCannibals(), "bfs", repeated="explored")
    assert tree.goal.depth == 11
    path = [n.state for n in tree.goal.path()]
    assert all(MissionariesCannibals().is_valid(s) for s in path)
    assert state_space(MissionariesCannibals())["reachable"] == 16


def test_rotating_workforce_dfs_finds_valid_cyclic_schedule():
    problem = RotatingWorkforce()
    tree = build_tree(problem, "dfs", repeated="none")
    assert tree.goal is not None and tree.goal.depth == 7
    sequence = "".join(problem.rows(tree.goal.state))
    assert check(sequence, problem.inst, cyclic=True) == []
    # daily demand: one D and one N every day
    for column in tree.goal.state:
        assert sorted(column) == sorted("DN-")


def test_rws_checks_detect_violations():
    problem = RotatingWorkforce()
    assert "forbidden N->D" in check("ND", problem.inst, cyclic=False)
    assert any("longer" in v for v in check("DDDDD", problem.inst, cyclic=False))
    assert any("shorter" in v for v in check("-N-", problem.inst, cyclic=False))


def test_every_figure_exports_dot():
    for name in ["8puzzle_full_depth3", "mc_bfs_graph", "rws_full_depth2"]:
        tree, title, rankdir = build_figure(name)
        dot = to_dot(tree, title, rankdir)
        assert dot.startswith("digraph") and dot.count("->") >= len(tree.nodes) - 1


def test_rws_cyclic_check_wraps_from_last_row_to_first():
    problem = RotatingWorkforce()
    sequence = "DD--NN"  # read cyclically, the final N is followed by the first D
    assert "forbidden N->D" not in check(sequence, problem.inst, cyclic=False)
    assert "forbidden N->D" in check(sequence, problem.inst, cyclic=True)
