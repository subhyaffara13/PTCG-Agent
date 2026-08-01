
def _reduce_system_once(
    constraint_system: ConstraintSystem,
) -> ConstraintSystem | Unsatisfiable | None:
  """Performs one reduction step over each constraint in a constraint system.

  Returns:
    - Unsatisfiable(): if the constraint system is unsatisfiable.
    - A new constraint system if any constraint was reduced.
    - None: if the constraint system is not known unsatisfiable, but hasn't been
      reduced.
  """
  assignments = constraint_system.assignments
  constraints: list[Constraint] = []
  changed = False

  def try_assign(var: Variable, cst: Constant) -> bool:
    if var in assignments and assignments[var] != cst:
      return False
    if not is_valid_assignment(var, cst):
      return False
    assignments[var] = cst
    return True

  for constraint in constraint_system.constraints:
    match reduce_constraint(constraint, assignments):
      case Unsatisfiable():
        return Unsatisfiable()
      case Equals(lhs=Variable() as var, rhs=cst) if isinstance(cst, Constant):
        if not try_assign(var, cst):
          return Unsatisfiable()
        changed = True
      case Equals(lhs=cst, rhs=Variable() as var) if isinstance(cst, Constant):
        if not try_assign(var, cst):
          return Unsatisfiable()
        changed = True
      case new_constraint:
        match new_constraint.holds():  # pyrefly: ignore[missing-attribute]
          case None:
            constraints.append(new_constraint)  # pyrefly: ignore[bad-argument-type]
            changed |= new_constraint != constraint
          case False:
            return Unsatisfiable()
          case True:
            changed = True

  new_constraints = _merge_all_divides_constraints(constraints)
  changed |= len(new_constraints) != len(constraints)
  constraints = new_constraints

  # Shortcut for a specific case of unsatisfiability. This shortcut
  # drastically reduces the size of the search space.
  if _has_relayout_of_non_splat_to_splat(constraints):
    return Unsatisfiable()

  if changed:
    return ConstraintSystem(
        assignments=assignments | constraint_system.assignments,
        constraints=constraints,
    )
  return None

