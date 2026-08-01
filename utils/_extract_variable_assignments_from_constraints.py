
def _extract_variable_assignments_from_constraints(
    constraints: Sequence[cs.Constraint], arch: tuple[int, int],
) -> Iterator[tuple[cs.Variable, cs.Constant]]:
  """Attempts to extract variable assignments from all constraints."""
  dpv = _divides_per_var(constraints)
  def priority(constraint: cs.Constraint) -> int:
    match constraint:
      # We want to minimize the number of relayouts in the kernel, so we first
      # try to satisfy relayout constraints via identity relayouts.
      case cs.Relayout():
        return 0  # Highest priority
      case _:
        return 1
  for c in sorted(constraints, key=priority):
    match c:
      case cs.IsTransferableTmemRegisters():
        yield from _extract_layout_candidates_from_tmem_registers_transfer(c)
      case cs.IsTransferableSmemRegisters():
        yield from _extract_layout_candidates_from_smem_registers_transfer(c, dpv, arch)
      case cs.Equals(cs.Reduce(cs.Variable() as large, axes=axes, keep_dims=keep_dims), cs.RegisterLayout() as small):
        for layout in extract_assignment_candidates_from_reduce_equation(small, large, axes, keep_dims):
          yield large, layout
      case cs.Equals(cs.RegisterLayout() as small, cs.Reduce(cs.Variable() as large, axes=axes, keep_dims=keep_dims)):
        for layout in extract_assignment_candidates_from_reduce_equation(small, large, axes, keep_dims):
          yield large, layout
      case cs.Relayout(cs.Variable() as var, cs.RegisterLayout() as layout):
        yield var, layout
      case cs.Relayout(cs.RegisterLayout() as layout, cs.Variable() as var):
        yield var, layout
      case cs.IsValidMmaTiling() as mma_tiling:
        yield from _extract_layout_candidates_from_mma_tiling(mma_tiling)
      case cs.IsSupportedBroadcast(cs.RegisterLayout() as src, cs.Variable() as dst, dims=dims):
        yield from _extract_layout_candidates_from_broadcast(src, dst, dims)

