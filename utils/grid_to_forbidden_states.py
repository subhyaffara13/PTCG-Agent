
def grid_to_forbidden_states(grid):
  """Converts a grid into string representation of forbidden states.

  Args:
    grid: Rows of the grid. '#' character denotes a forbidden state. All rows
      should have the same number of columns, i.e. cells.

  Returns:
    String representation of forbidden states in the form of x (column) and y
    (row) pairs, e.g. [1|1;0|2].
  """
  forbidden_states = []
  num_cols = len(grid[0])
  for y, row in enumerate(grid):
    assert len(row) == num_cols, f"Number of columns should be {num_cols}."
    for x, cell in enumerate(row):
      if cell == "#":
        forbidden_states.append(f"{x}|{y}")
  return "[" + ";".join(forbidden_states) + "]"


def grid_to_forbidden_states(grid: Sequence[str]) -> str:
  """Converts a grid into string representation of forbidden states.

  Args:
    grid: Rows of the grid. '#' character denotes a forbidden state. All rows
      should have the same number of columns, i.e. cells.

  Returns:
    String representation of forbidden states in the form of x (column) and y
    (row) pairs, e.g. [1|1;0|2].
  """
  forbidden_states = []
  num_cols = len(grid[0])
  for y, row in enumerate(grid):
    assert len(row) == num_cols, f'Number of columns should be {num_cols}.'
    for x, cell in enumerate(row):
      if cell == '#':
        forbidden_states.append(f'{x}|{y}')
  return '[' + ';'.join(forbidden_states) + ']'

