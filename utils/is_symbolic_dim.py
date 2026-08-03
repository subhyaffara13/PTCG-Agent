from typing import Any

def is_symbolic_dim(v: Any) -> bool:
  """Checks if a value is a symbolic dimension used for shape polymorphism.

  This should be used very rarely, because symbolic dimensions overload all
  operators, and should just work.
  """
  return getattr(v, "dimension_as_value", None) is not None


def is_symbolic_dim(p: DimSize) -> TypeGuard[_DimExpr]:
  """Checks if a dimension is symbolic.
  """
  return isinstance(p, _DimExpr)

