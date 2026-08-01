
def _scatter_mul_jvp_rhs(g, x, i, y, *, dimension_numbers,
                         indices_are_sorted, unique_indices, mode, **kw):
  if not unique_indices:
    raise NotImplementedError(
      "scatter_mul gradients are only implemented if `unique_indices=True`")
  return lax.mul(x, scatter_add(
      ad_util.zeros_like_jaxval(x), i, g, dimension_numbers=dimension_numbers,
      indices_are_sorted=indices_are_sorted, unique_indices=unique_indices,
      mode=mode))

