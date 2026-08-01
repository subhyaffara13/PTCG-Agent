
def _get_padded_shape(
    logical_shape: tuple[int, ...], dtype: jnp.dtype
) -> tuple[int, ...]:
  # Do not pad scalars.
  if logical_shape == ():
    return ()

  # TODO(nrink): Replace this assertion with raising an exception early if
  # dtype `float64` is used in TPU interpret mode. (`float64` has itemsize
  # of 8, and an itemsize > 4 will cause infinite looping in `infer_tiling`.)
  assert dtype.itemsize <= 4
  tile_shape = tpu_info.infer_tiling(
      jax.core.ShapedArray(shape=logical_shape, dtype=dtype)
  )

  result = []
  for dim, tile_dim in zip(logical_shape, tile_shape):
    # `tpu_info.infer_tiling` returns a tuple of `None` if its argument has no
    # `dtype` attribute (but we did pass a `dtype` above).
    assert tile_dim is not None
    result.append(((dim + tile_dim - 1) // tile_dim) * tile_dim)
  return tuple(result)

