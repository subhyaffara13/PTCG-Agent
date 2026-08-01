
def _normalize_set(
    values: Iterable[str], default: Iterable[str], valid: Iterable[str]
) -> set[str]:
  # Normalize str -> list (e.g. skip='torch')
  values = [values] if isinstance(values, str) else values
  values = set(default if values is None else values)
  if extra_elements := (values - set(valid)):
    raise ValueError(f'Unexpected numpy module: {extra_elements}')
  return values

