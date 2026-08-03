from typing import Any

def is_dim(d: object) -> bool:
    return isinstance(d, (DVar, int)) or d == Dyn


def is_dim(v: Any) -> bool:
  return is_symbolic_dim(v) or is_constant_dim(v)

