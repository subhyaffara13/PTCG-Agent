
def zeros_like_spec(spec: jax.ShapeDtypeStruct) -> jax.Array:
  """Builds a zero-valued array matching the given spec without global allocs."""

  def _zeros(index: tuple[slice | int, ...] | None) -> np.ndarray:
    assert index is not None
    local_shape = []
    for dim, size in zip(index, spec.shape):
      if isinstance(dim, slice):
        start = 0 if dim.start is None else dim.start
        stop = size if dim.stop is None else dim.stop
        local_shape.append(stop - start)
      else:
        local_shape.append(1)
    return np.zeros(tuple(local_shape), dtype=spec.dtype)

  return jax.make_array_from_callback(
      spec.shape, spec.sharding, _zeros, dtype=spec.dtype
  )

