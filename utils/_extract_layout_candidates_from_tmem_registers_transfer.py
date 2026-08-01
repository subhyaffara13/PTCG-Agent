
def _extract_layout_candidates_from_tmem_registers_transfer(
    constraint: cs.IsTransferableTmemRegisters,
) -> Iterator[tuple[cs.Variable, cs.Constant]]:
  match constraint.source, constraint.target:
    case cs.Variable() as src, tgt if isinstance(tgt, cs.Constant):
      variable, constant = src, tgt
    case src, cs.Variable() as tgt if isinstance(src, cs.Constant):
      variable, constant = tgt, src
    case _:
      return

  columns = constraint.shape[1]

  if isinstance(constant, cs.TMEMLayout):
    candidates = [
      fa.TCGEN05_LAYOUT,
      constant.value.as_tiled_layout(),
      fa.TMEM_NATIVE_LAYOUT,
      fa.WGMMA_LAYOUT,
    ]
    if columns % 16 == 0:
      candidates.append(tcgen05.fa_m64_collective_layout(columns))
    for candidate in candidates:
     if constraint.is_valid_tmem_transfer(constant.value, candidate):
       yield variable, cs.RegisterLayout(candidate)
    return

  assert isinstance(constant, cs.RegisterLayout)
  if not isinstance(constant.value, fa.TiledLayout):
    return
  for packing in dict.fromkeys([32 // constraint.bitwidth, 1]):
    candidates = [tcgen05.tmem_default_layout(packing)]
    if columns % 16 == 0 and packing <= columns // 2:
      candidates.append(tcgen05.tmem_half_lane_layout(columns, packing))
    if columns % 16 == 0 and packing <= 8:
      candidates.append(tcgen05.tmem_m64_collective_layout(columns, packing))
    for candidate in candidates:
      if constraint.is_valid_tmem_transfer(candidate, constant.value):
        yield variable, cs.TMEMLayout(candidate)

