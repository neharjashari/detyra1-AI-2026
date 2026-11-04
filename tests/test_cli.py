import pytest

from uninformed_search.cli import main

WIKIPEDIA_PUZZLE = "53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79"


@pytest.mark.parametrize(
    "argv",
    [
        ["golfers", "-w", "3"],
        ["golfers", "-g", "2", "-p", "2", "--max-weeks"],
        ["golfers", "--landscape", "-w", "10"],
        ["sudoku", "--level", "easy"],
        ["sudoku", "--puzzle", WIKIPEDIA_PUZZLE, "--landscape"],
        ["latin", "-n", "4", "-v"],
        ["latin", "-n", "5", "--landscape"],
        ["trees", "--ascii", "rws_dfs"],
    ],
)
def test_commands_succeed(argv, capsys):
    assert main(argv) == 0
    assert capsys.readouterr().out


def test_invalid_group_size_is_an_argument_error():
    with pytest.raises(SystemExit):
        main(["golfers", "-p", "1"])


@pytest.mark.parametrize("puzzle", ["123", "11" + "." * 79])
def test_invalid_puzzle_is_an_argument_error(puzzle, capsys):
    with pytest.raises(SystemExit):
        main(["sudoku", "--puzzle", puzzle])

    assert "argument --puzzle" in capsys.readouterr().err


def test_trees_without_graphviz_warns_and_fails(tmp_path, monkeypatch, capsys):
    monkeypatch.setattr("shutil.which", lambda name: None)

    code = main(["trees", "--out", str(tmp_path)])

    assert code == 1
    assert "Graphviz" in capsys.readouterr().err
