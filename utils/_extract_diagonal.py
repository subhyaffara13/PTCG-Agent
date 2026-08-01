
def _extract_diagonal(s: Array) -> Array:
  """Extract the diagonal from a batched matrix"""
  i = lax.iota('int32', min(s.shape[-2], s.shape[-1]))
  return s[..., i, i]

