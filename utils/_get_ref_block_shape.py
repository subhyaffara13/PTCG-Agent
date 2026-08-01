
def _get_ref_block_shape(block_shape: tuple[BlockDim, ...]) -> tuple[int, ...]:
  # Special handling for squeezed here (don't include Squeezed dims in the Ref
  # shape).
  return tuple(
      _get_block_dim_size(dim)
      for dim in block_shape
      if not isinstance(dim, Squeezed)
  )

