
def _dct_interleave(x: Array, axis: int) -> Array:
  v0 = lax.slice_in_dim(x, None, None, 2, axis)
  v1 = lax.rev(lax.slice_in_dim(x, 1, None, 2, axis), (axis,))
  return lax.concatenate([v0, v1], axis)

