
def _block_transforms_equal(
    bs1: BlockIndexTransform | NoBlockIndexTransform,
    bs2: BlockIndexTransform | NoBlockIndexTransform,
    block_idxs_avals: tuple[tuple[core.AbstractValue, ...], ...],
    strict_mode: bool = True,
) -> bool:
  if bs1 is bs2:
    return True
  if isinstance(bs1, BlockIndexTransform) and isinstance(
      bs2, BlockIndexTransform
  ):
    value = _block_shapes_equal(
        bs1.block_shape, bs2.block_shape
    )
    if strict_mode:
      value = value and _compare_index_transforms(
          bs1.block_index_transform, bs2.block_index_transform, block_idxs_avals
      )
    return value
  return False

