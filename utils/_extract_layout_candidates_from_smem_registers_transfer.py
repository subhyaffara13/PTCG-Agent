
def _extract_layout_candidates_from_smem_registers_transfer(
    constraint: cs.IsTransferableSmemRegisters,
    division_constraint_per_var: dict[cs.Variable, cs.Divides],
    arch: tuple[int, int]
) -> Iterator[tuple[cs.Variable, cs.Constant]]:
  src, tgt = constraint.source, constraint.target
  match src, tgt:
    case cs.Variable(), cst if isinstance(cst, cs.Constant):
      variable, constant = src, tgt
    case cst, cs.Variable() if isinstance(cst, cs.Constant):
      variable, constant = tgt, src
    case _:
      return

  assert isinstance(variable, cs.Variable)  # Satisfy type checkers.
  if isinstance(constant, cs.RegisterLayout):
    layout = constant.value
    assert variable.memory_space == cs.MemorySpace.SMEM
    if isinstance(layout, fa.TiledLayout) and len(variable.shape) >= 2:
      # Maintain a set of yielded tilings to avoid duplicates caused by existing
      # divides constraints.
      yielded = set()
      divide_constraint = division_constraint_per_var.get(variable)
      for tiling in _conjure_tilings_for_smem_ref(variable.key.value.type):
        if divide_constraint is not None:
          # Apply existing multiplicity constraints to the conjured tiling.
          tiling = cs.merge_divides_constraints(
              divide_constraint, cs.Divides(variable, tiling)
          ).tiling_multiple
        if tiling in yielded:
          continue
        yielded.add(tiling)
        yield variable, cs.SMEMTransforms(lc.TileTransform(tiling))
    return

  assert isinstance(constant, cs.SMEMTransforms)
  assert variable.memory_space == cs.MemorySpace.REG
  for layout in _register_layouts_for_optimized_transfer_to_smem(
      variable.key.value.type, constant, arch
  ):
    yield variable, cs.RegisterLayout(layout)

