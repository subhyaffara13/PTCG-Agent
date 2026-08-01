
def _divides_per_var(
    constraints: Sequence[cs.Constraint],
) -> dict[cs.Variable, cs.Divides]:
  result: dict[cs.Variable, cs.Divides] = {}
  for constraint in constraints:
    if isinstance(constraint, cs.Divides) and isinstance(
        constraint.expr, cs.Variable
    ):
      assert constraint.expr not in result
      result[constraint.expr] = constraint
  return result

