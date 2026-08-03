import math


def _print_columns(strings):
  """Prints a list of strings in columns."""
  padding = 2
  longest = max(len(s) for s in strings)
  max_columns = math.floor((_MAX_WIDTH - 1) / (longest + 2 * padding))
  rows = math.ceil(len(strings) / max_columns)
  columns = math.ceil(len(strings) / rows)  # Might not fill all max_columns.
  for r in range(rows):
    for c in range(columns):
      i = r + c * rows
      if i < len(strings):
        print(" " * padding + strings[i].ljust(longest + padding), end="")
    print()

