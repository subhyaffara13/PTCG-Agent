
def _construct_diagonal(s: Array) -> Array:
  """Construct a (batched) diagonal matrix"""
  i = lax.iota('int32', s.shape[-1])
  return lax.full((*s.shape, s.shape[-1]), 0, s.dtype).at[..., i, i].set(s)

