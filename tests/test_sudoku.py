import pytest

from uninformed_search import sudoku

PUZZLES = [(level, name, puzzle) for level in sudoku.LEVELS for name, puzzle in sudoku.load_puzzles(level)]


@pytest.mark.parametrize("level, name, puzzle", PUZZLES)
def test_bfs_solves_bundled_puzzles(level, name, puzzle):
    result = sudoku.solve_bfs(puzzle)

    assert result.status == "solved"
    assert sudoku.is_solution(result.solution, puzzle)


@pytest.mark.parametrize("level, name, puzzle", PUZZLES)
def test_bundled_puzzles_are_in_the_right_level(level, name, puzzle):
    assert sudoku.level_of(puzzle) == level


def test_every_level_has_puzzles():
    assert all(sudoku.load_puzzles(level) for level in sudoku.LEVELS)


def test_unsolvable_puzzle_is_reported_as_failure():
    # the givens do not repeat, but cell (0, 8) has no allowed digit left
    puzzle = sudoku.parse("12345678." + "........9" + "." * 63)

    assert sudoku.solve_bfs(puzzle).status == "failure"


def test_puzzle_with_repeated_given_is_rejected():
    puzzle = sudoku.parse("11" + "." * 79)

    with pytest.raises(ValueError):
        sudoku.solve_bfs(puzzle)


def test_parse_accepts_zeros_and_separators():
    text = "0" * 9 + " | " + "1" + "." * 71

    assert sudoku.parse(text) == "." * 9 + "1" + "." * 71


def test_parse_rejects_wrong_length():
    with pytest.raises(ValueError):
        sudoku.parse("123")


def test_allowed_digits_respect_row_column_and_box():
    # cell 2 = row 0, column 2: row has 1 and 2, column has 3 (row 4), box has 4 (row 1)
    grid = sudoku.parse("12......." + "4........" + "." * 18 + "..3......" + "." * 36)

    assert sudoku.allowed_digits(grid, 2) == ["5", "6", "7", "8", "9"]


def test_objective_is_zero_only_for_a_solved_grid():
    puzzle = sudoku.load_puzzles("easy")[0][1]
    solution = sudoku.solve_bfs(puzzle).solution
    swapped = solution[1] + solution[0] + solution[2:]  # swap two cells of the first row

    assert sudoku.objective(solution) == 0
    assert sudoku.objective(swapped) > 0


def test_landscape_counts_the_empty_cells():
    land = sudoku.landscape("." * 80 + "1")

    assert land["empty_cells"] == 80
    assert land["any_digit_in_every_empty_cell"] == 9**80
