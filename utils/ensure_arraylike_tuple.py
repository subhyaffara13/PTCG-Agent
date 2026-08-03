from typing import Any

def ensure_arraylike_tuple(fun_name: str, tup: Sequence[Any]) -> tuple[Array, ...]:
  """Check that argument elements are arraylike and convert to a tuple of arrays.

  This is useful because ensure_arraylike with a single argument returns a single array.
  """
  check_arraylike(fun_name, *tup)
  return tuple(_arraylike_asarray(arg) for arg in tup)

