
def _safe_normalize(x, thresh=None):
  """
  Returns the L2-normalized vector (which can be a pytree) x, and optionally
  the computed norm. If the computed norm is less than the threshold `thresh`,
  which by default is the machine precision of x's dtype, it will be
  taken to be 0, and the normalized x to be the zero vector.
  """
  norm = _norm(x)
  dtype, weak_type = dtypes.lattice_result_type(*tree_leaves(x))
  if thresh is None:
    thresh = dtypes.finfo(norm.dtype).eps
  thresh = thresh.astype(dtype).real

  use_norm = norm > thresh

  norm_cast = lax_internal._convert_element_type(norm, dtype, weak_type)
  normalized_x = tree_map(lambda y: jnp.where(use_norm, y / norm_cast, 0.0), x)
  norm = jnp.where(use_norm, norm, 0.0)
  return normalized_x, norm

