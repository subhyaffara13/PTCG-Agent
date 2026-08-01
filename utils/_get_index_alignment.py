
def _get_index_alignment(block_mapping: BlockMapping) -> tuple[int, ...]:
  def _get_bdim_alignment(b: pallas_core.BlockDim):
    match b:
      case pallas_core.Squeezed() | pallas_core.Element():
        return 1
      case pallas_core.Blocked():
        return b.block_size
  return tuple(_get_bdim_alignment(b) for b in block_mapping.block_shape)

