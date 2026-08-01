
def _get_block_shape(block_shape: tuple[BlockDim, ...]) -> tuple[int, ...]:
  return tuple(_get_block_dim_size(dim) for dim in block_shape)


def _get_block_shape(spec: pallas_core.BlockSpec) -> tuple[int, ...]:
  """Get the block shape for a given block spec."""
  def _get_dim_size(bd):
    match bd:
      case int():
        return bd
      case None | Squeezed():
        return None
      case (
          Blocked(block_size)
          | Element(block_size)
          | BoundedSlice(block_size)
          | Indirect(block_size)
      ):
        return block_size
      case _:
        raise ValueError(f"Unsupported block dimension type: {bd}")
  if spec.block_shape is None:
    raise ValueError("Block shape must be specified.")
  block_shape_nones = tuple(_get_dim_size(x) for x in spec.block_shape)
  return tuple(x for x in block_shape_nones if x is not None)


def _get_block_shape(spec: pallas_core.BlockSpec, ref_shape: tuple[int, ...]):
  if spec.block_shape is None:
    return ref_shape

  block_shape = tuple(
      _get_block_size(bd)
      for bd in spec.block_shape
      if not (bd is None or isinstance(bd, pl.Squeezed))
  )
  return block_shape

