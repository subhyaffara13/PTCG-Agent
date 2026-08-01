
def saturate_divides_constraints_for_equal_vars(
    system: ConstraintSystem,
) -> ConstraintSystem:
  """Saturates Divides constraints between all transitively equal vars."""
  equal_vars = compute_transitively_equal_vars(system)
  new_constraints: list[Constraint] = []
  for constraint in system.constraints:
    new_constraints.append(constraint)
    match constraint:
      case Divides(expr=expr, tiling_multiple=tiling_multiple):
        if isinstance(expr, Variable):
          for equal_var in equal_vars.get(expr, []):
            new_constraints.append(Divides(equal_var, tiling_multiple))
      case _:
        pass
  new_constraints = _merge_all_divides_constraints(new_constraints)
  return dataclasses.replace(system, constraints=new_constraints)

