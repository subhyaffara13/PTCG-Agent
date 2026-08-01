
def supported_shapes(dtype: jax.typing.DTypeLike) -> Sequence[tuple[int, ...]]:
  """Returns all supported array shapes for the given dtype on SparseCore."""
  sc_info = get_sparse_core_info()
  num_lanes = sc_info.num_lanes
  itemsize = jnp.dtype(dtype).itemsize
  if itemsize > 4:
    raise ValueError(f"Unsupported dtype: {dtype}")
  packing_factor = 4 // itemsize
  if packing_factor == 1:
    return [(num_lanes,)]
  return [(num_lanes * packing_factor,), (packing_factor, num_lanes)]

