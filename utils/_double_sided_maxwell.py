
def _double_sided_maxwell(key, loc, scale, shape, dtype) -> Array:
  params_shapes = lax.broadcast_shapes(np.shape(loc), np.shape(scale))
  if not shape:
    shape = params_shapes

  shape = shape + params_shapes
  maxwell_key, rademacher_key = _split(key)
  maxwell_rvs = maxwell(maxwell_key, shape=shape, dtype=dtype)
  # Generate random signs for the symmetric variates.
  random_sign = rademacher(rademacher_key, shape=shape, dtype=dtype)
  assert random_sign.shape == maxwell_rvs.shape

  return random_sign * maxwell_rvs * scale + loc

