
def _get_sorted_leaves(
  xs: tp.Mapping[tp.Any, tp.Any],
) -> list[tp.Any]:
  if not isinstance(xs, tp.Mapping):  # type: ignore
    raise TypeError(f'expected Mapping; got {type(xs).__qualname__}')
  leaves: list[tp.Any] = []

  def _flatten(xs):
    if not isinstance(xs, tp.Mapping):
      leaves.append(xs)
    else:
      for _, value in sorted(xs.items()):
        _flatten(value)

  _flatten(xs)
  return leaves

