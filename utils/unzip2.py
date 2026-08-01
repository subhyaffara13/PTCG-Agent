
def unzip2(xys: Iterable[tuple[T1, T2]]
    ) -> tuple[tuple[T1, ...], tuple[T2, ...]]:
  """Unzip sequence of length-2 tuples into two tuples."""
  # Note: we deliberately don't use zip(*xys) because it is lazily evaluated,
  # is too permissive about inputs, and does not guarantee a length-2 output.
  xs: list[T1] = []
  ys: list[T2] = []
  for x, y in xys:
    xs.append(x)
    ys.append(y)
  return tuple(xs), tuple(ys)

