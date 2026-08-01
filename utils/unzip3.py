
def unzip3(xyzs: Iterable[tuple[T1, T2, T3]]
    ) -> tuple[tuple[T1, ...], tuple[T2, ...], tuple[T3, ...]]:
  """Unzip sequence of length-3 tuples into three tuples."""
  # Note: we deliberately don't use zip(*xyzs) because it is lazily evaluated,
  # is too permissive about inputs, and does not guarantee a length-3 output.
  xs: list[T1] = []
  ys: list[T2] = []
  zs: list[T3] = []
  for x, y, z in xyzs:
    xs.append(x)
    ys.append(y)
    zs.append(z)
  return tuple(xs), tuple(ys), tuple(zs)

