
def print_columns(strings, max_width=MAX_WIDTH):
  """Prints a list of strings in columns."""
  padding = 2
  shortest = min(len(s) for s in strings)
  max_columns = max(1, math.floor((max_width - 1) / (shortest + 2 * padding)))
  for cols in range(max_columns, 0, -1):
    rows = math.ceil(len(strings) / cols)
    chunks = [strings[i : i + rows] for i in range(0, len(strings), rows)]
    col_widths = [max(len(s) for s in chunk) for chunk in chunks]
    if sum(col_widths) + 2 * padding * len(col_widths) <= max_width:
      break
  for r in range(rows):
    for c in range(cols):
      i = r + c * rows
      if i < len(strings):
        print(" " * padding + strings[i].ljust(col_widths[c] + padding), end="")
    print()

