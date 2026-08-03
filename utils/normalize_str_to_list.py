from typing import Optional

def normalize_str_to_list(x: Optional[StrOrStrList]) -> list[str]:
  if x is None:
    return []
  elif isinstance(x, str):
    return [v.strip() for v in x.split(',')]
  elif not isinstance(x, (list, tuple)):
    raise TypeError(f'Expected list. Got: {x!r}')
  else:  # list/tuple
    return list(x)

