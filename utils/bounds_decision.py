
def bounds_decision(e: DimSize,
                    prec: BoundsPrecision) -> tuple[float, float]:
  if not isinstance(e, _DimExpr):
    return (int(e), int(e))
  decision = _DecisionByElimination.build(e.scope)
  return decision.bounds(e, prec, add_implicit_constraints=True)

