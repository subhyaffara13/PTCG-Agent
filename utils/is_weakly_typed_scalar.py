from typing import Any

def is_weakly_typed_scalar(x: Any) -> bool:
  try:
    return x.aval.weak_type and np.ndim(x) == 0
  except AttributeError:
    return type(x) in python_scalar_types

