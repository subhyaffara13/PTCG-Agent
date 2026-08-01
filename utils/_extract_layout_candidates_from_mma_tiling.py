
def _extract_layout_candidates_from_mma_tiling(
    mma_tiling: cs.IsValidMmaTiling,
) -> Iterator[tuple[cs.Variable, cs.Constant]]:
  v: cs.Variable
  match mma_tiling.expr:
    case cs.Variable() as var:
      is_transposed = False
      v = var
    case cs.Transpose(cs.Variable() as var):
      assert isinstance(var, cs.Variable)
      is_transposed = True
      v = var
    case _:
      return

  tiled_dimensions = v.shape[-2:]
  # TODO(bchetioui): we can conjure additional tilings here if
  # `allow_unswizzled` is true, but it is not clear which ones yet.
  for swizzle in (128, 64, 32):
    swizzle_elems = swizzle * 8 // mma_tiling.bitwidth
    tiling = (swizzle_elems, 8) if is_transposed else (8, swizzle_elems)
    if any(s % t for s, t in zip(tiled_dimensions, tiling)):
      continue
    yield v, cs.SMEMTransforms(lc.TileTransform(tiling))

