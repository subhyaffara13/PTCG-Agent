
def _canonicalize_block_shape(block_shape: Sequence[BlockDim | int | None]
                              ) -> tuple[BlockDim, ...]:
  return tuple(_canonicalize_block_dim(dim) for dim in block_shape)

