
def _create_bounded_slice(slice_start: jax.Array | int,
                          slice_size: jax.Array | int,
                          block_size: int,
                          dim_size: int,
                          tiling: int | None):
  if tiling is not None and block_size % tiling != 0:
    raise ValueError(f"Block size must divide tiling: {block_size=}, {tiling=}")
  # We assume by construction that slice_size <= block_size. We also assume
  # that the slice_start is already aligned to the tiling.

  if tiling is None:
    return ds(slice_start, slice_size)

  # If we are out of bound, we need to round the slice size down to the nearest
  # multiple of the tiling.
  is_oob = slice_start + slice_size > dim_size
  remaining = dim_size - slice_start
  rounded_size = jnp.where(is_oob, align_to(remaining, tiling), slice_size)
  rounded_size = multiple_of(rounded_size, tiling)
  return ds(slice_start, rounded_size)

