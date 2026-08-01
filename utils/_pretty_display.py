
def _pretty_display(x):
  """Print `x` and return `x`."""
  # 2 main use-case:
  # * Print strings (including `\n`)
  # * Pretty-print dataclasses
  if isinstance(x, str):
    print(x)
  else:
    print(epy.pretty_repr(x))

