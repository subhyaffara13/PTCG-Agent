
def _canonicalize_tuple(x: Sequence[int] | int) -> tuple[int, ...]:
  if isinstance(x, Iterable):
    return tuple(x)
  else:
    return (x,)


def _canonicalize_tuple(x: tp.Sequence[int] | int) -> tuple[int, ...]:
  if isinstance(x, tp.Iterable):
    return tuple(x)
  else:
    return (x,)

