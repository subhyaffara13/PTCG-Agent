
def find_assignments_for(
    unknowns: Sequence[cs.Variable],
    constraint_system: cs.ConstraintSystem,
    *,
    fuel: int,
    arch: tuple[int, int],
) -> tuple[dict[cs.Variable, cs.Constant] | cs.Unsatisfiable, int]:
  """Attempts to find assignments that satisfy `constraint_system` for `unknowns`.

  Args:
    unknowns: The set of variables that are unknown. Represented as a sequence
      of `Variable`s for determinism purposes.
    constraint_system: the constraint system to satisfy.
    fuel: The fuel to use for the search. Once the fuel is exhausted, we raise
      an error.
    arch: The architecture to target in the search.

  Returns:
    A tuple where the first element is the solution, and the second element is
    the fuel remaining after the search. The solution is either:
      - Unsatisfiable() if the constraint system has unsatisfiable constraints.
      - A dictionary assigning all the unknown variables to
        `ConstantExpression`s such that the assignment satisfies the constraint
        system otherwise.
  """
  if isinstance(result := cs.reduce(constraint_system), cs.Unsatisfiable):
    return cs.Unsatisfiable(), fuel

  constraint_system = result
  remaining_unknowns = [
      u for u in unknowns if u not in constraint_system.assignments.keys()
  ]

  # In this case, we have determined an assignment for all the unknown
  # variables. Return their respective assignment.
  if not remaining_unknowns:
    assert not constraint_system.constraints, (
        "A satisfiable system should not have remaining unsatisfied"
        " constraints. This is a bug."
    )
    return {
        v: k for v, k in constraint_system.assignments.items() if v in unknowns
    }, fuel

  # If unknowns remain and we have fully reduced the system, we may still
  # be able to make progress by trying out potential assignments. These
  # new assignments could make the system unsatisfiable, so we use a recursive
  # call to be able to backtrack if necessary.
  for assignment in conjure_assignment(
      remaining_unknowns, constraint_system, arch
  ):
    if fuel <= 0:
      raise ValueError(
          "Layout inference failed to find a solution. Consider adding layout "
          "annotations to your program to guide the search."
      )
    variable, expr = assignment
    assert isinstance(expr, cs.Constant)
    if not cs.is_valid_assignment(variable, expr):
      continue
    # Trying one valid assignment consumes fuel.
    fuel -= 1
    new_constraint_system = (
        cs.ConstraintSystem(assignments={variable: expr}) & constraint_system
    )
    if isinstance(new_constraint_system, cs.Unsatisfiable):
      # This assignment is not compatible with the constraint system.
      continue
    solution, fuel = find_assignments_for(
        unknowns, new_constraint_system, fuel=fuel, arch=arch
    )
    if not isinstance(solution, cs.Unsatisfiable):
      return solution, fuel

  # TODO(bchetioui): should we have a way to give a useful dump to the user
  # here, perhaps indicating what to layout cast.
  return cs.Unsatisfiable(), fuel

