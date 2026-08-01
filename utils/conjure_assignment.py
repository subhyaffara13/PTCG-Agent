
def conjure_assignment(
    unknowns: Sequence[cs.Variable],
    constraint_system: cs.ConstraintSystem,
    arch: tuple[int, int],
) -> Iterator[tuple[cs.Variable, cs.Constant]]:
  """Attempts to conjure an assignment for an unknown variable."""
  # TODO(allanrenucci): We should be able to short-circuit the search here if
  # the constraint is not satisfiable.

  # As we extract assignment candidates from constraints, we prioritize
  # candidates that are more "interesting"; e.g., in the case of registers,
  # introducing splat layout candidate assignments often leads to a dead end in
  # practice---as opposed to tiled layouts, which are more likely to yield
  # solutions to the constraint system.
  low_priority_assignments: list[tuple[cs.Variable, cs.Constant]] = []
  for variable, constant in _extract_variable_assignments_from_constraints(
      constraint_system.constraints, arch
  ):
    match constant:
      case cs.RegisterLayout(value=value) if not isinstance(
          value, fa.TiledLayout
      ):
        low_priority_assignments.append((variable, constant))
      case _:
        yield variable, constant

  # After all high-priority assignments have been attempted, switch to using
  # low-priority assignments.
  for variable, constant in low_priority_assignments:
    yield variable, constant

  # Here, we have not managed to find an assignment for all the unknown
  # variables. We now try to introduce new arbitrary (valid) assignments into
  # the system, and hope that they turn out to be compatible with the constraint
  # system.
  for variable in unknowns:
    if variable in constraint_system.assignments:
      continue
    # Try to instantiate a single variable to a default layout and see if it
    # reduces the system.
    match variable.memory_space:
      case cs.MemorySpace.REG:
        layout = _strided_layout_for_variable(variable)
        if layout is not None:
          yield variable, cs.RegisterLayout(layout)
      case cs.MemorySpace.SMEM:
        yield variable, cs.SMEMTransforms(None)
      case cs.MemorySpace.TMEM:
        layout = _default_tmem_layout_for_variable(variable)
        if layout is not None:
          yield variable, cs.TMEMLayout(layout)
      case never:
        assert_never(never)

