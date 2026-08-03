from typing import Any

def _convertible_to_poly(p: Any) -> bool:
  return isinstance(p, _DimExpr) or _convertible_to_int(p)

