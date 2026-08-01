
def saturate_distinct_from_splat(
    constraint_system: ConstraintSystem,
) -> ConstraintSystem | Unsatisfiable:
  """Adds transitive NotOfType constraints for all non-splat variables.

  Given `n` variables `l0`, ... `l{n-1}`, and a set of relayouts
  `{ Relayout(l{i}, l{i+1}) : 0 <= i < n }`, if we also know that
  `l{0}` is not splat, then we can automatically deduce that none of
  `l0`, ..., `l{n-1}` are splat either.

  This helps us quickly conclude that a system is unsatisfiable in cases where
  a non-splat variable is transitively relaid out into a splat layout.
  """
  non_splat = non_splat_variables(constraint_system.constraints)
  new_constraints: list[Constraint] = []
  new_non_splat_found = bool(non_splat)

  while new_non_splat_found:
    new_non_splat_found = False
    for constraint in constraint_system.constraints:
      match constraint:
        case Relayout(source=source, target=target):
          if (
              isinstance(target, Variable)
              and source in non_splat
              and target not in non_splat
          ):
            new_non_splat_found = True
            non_splat.add(target)
            new_constraints.append(NotOfType(target, fa.WGSplatFragLayout))
        case _:
          pass
  return constraint_system & ConstraintSystem(constraints=new_constraints)

