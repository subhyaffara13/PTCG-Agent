
def _hankel(c: Array, r: Array) -> Array:
  ncols, = c.shape
  nrows, = r.shape
  if ncols == 0 or nrows == 0:
    return jnp.empty((ncols, nrows), dtype=jnp.result_type(c, r))
  v = jnp.concatenate((c, r[1:]))
  return lax.conv_general_dilated_patches(
      v.reshape((1, ncols + nrows - 1, 1)),
      (nrows,), (1,), 'VALID',
      dimension_numbers=('NTC', 'IOT', 'NTC'),
      precision=lax.Precision.HIGHEST)[0]

