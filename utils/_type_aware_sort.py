
def _type_aware_sort(item: tuple[tp.Any, tp.Any]) -> tuple[int, tp.Any]:
  key, _ = item
  if isinstance(key, int):
    return (0, key)
  elif isinstance(key, str):
    return (1, key)
  else:
    raise ValueError(f'Unsupported key type: {type(key)!r}')

