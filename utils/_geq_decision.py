from typing import Callable

def _geq_decision(e1: DimSize, e2: DimSize, cmp_str: Callable[[], str]) -> bool:
  """Implements `e1 >= e2`.

  Args:
    e1, e2: the expressions to compare for greater-equal
    cmp_str: a callable such that `cmp_str()` describes the comparison
      for error messages, e.g., "a <= b". Without this all comparisons would
      be reported as ">=".

  Raises InconclusiveDimensionOperation if the result is not conclusive.
  """
  if isinstance(e1, _DimExpr):
    scope = e1.scope
    if isinstance(e2, _DimExpr):
      scope._check_same_scope(e2, f"when comparing {cmp_str()}")
  elif isinstance(e2, _DimExpr):
    scope = e2.scope
  else:
    return int(e1) >= int(e2)
  lb, ub = _bounds_decision(e1 - e2, BoundsPrecision.FOR_GEQ0_OR_LT0)
  if lb >= 0:
    return True
  if ub < 0:
    return False

  if scope._explicit_constraints:
    describe_scope = f"\nUsing symbolic scope {scope}"
  else:
    describe_scope = ""
  raise InconclusiveDimensionOperation(
      f"Symbolic dimension comparison {cmp_str()} is inconclusive.{describe_scope}")

