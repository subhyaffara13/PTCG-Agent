
def _merge_all_divides_constraints(constraints: Sequence[Constraint]) -> list[Constraint]:
  """Merges Divides constraints that can be merged."""
  result: list[Constraint] = []
  var_to_divides : dict[Variable, Divides] = {}
  for constraint in constraints:
    match constraint:
      case Divides(expr=Variable() as v) as d1:
        if (d0 := var_to_divides.get(v)) is None:
          var_to_divides[v] = d1
          continue
        var_to_divides[v] = merge_divides_constraints(d0, d1)
      case _:
        result.append(constraint)
  result.extend(var_to_divides.values())
  return result

