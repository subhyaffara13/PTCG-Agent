
def _create_blocked_slice(
    block_index: jax.Array | int,
    block_size: int,
    dim_size: int,
    tiling: int | None,
):
  block_start = block_size * block_index
  if (dim_rem := dim_size % block_size) == 0:
    return ds(block_start, block_size)
  if tiling is None:
    raise ValueError("If tiling is None, block_size must divide dim_size.")
  if block_size % tiling != 0:
    raise ValueError(f"Block size must divide tiling: {block_size=}, {tiling=}")
  num_blocks = cdiv(dim_size, block_size)
  is_last = block_index == num_blocks - 1
  rounded_size = jnp.where(
      is_last, align_to(dim_rem % block_size, tiling), block_size
  )
  rounded_size = multiple_of(rounded_size, tiling)
  return ds(block_index * block_size, rounded_size)

