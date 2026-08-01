
def non_splat_variables(
    constraints: Sequence[Constraint],
) -> set[Variable]:
  """Returns a all vars distinct from a splat."""
  vs: set[Variable] = set()
  for constraint in constraints:
    match constraint:
      case NotOfType(expr=Variable() as v, type=fa.WGSplatFragLayout):
        vs.add(v)
  return vs

