
def _toeplitz(c, r):
    # Form a 1-D array containing a reversed c followed by r[1:] that could be
    # strided to give us toeplitz matrix.
    vals = np.concatenate((c[::-1], r[1:]))
    out_shp = len(c), len(r)
    n = vals.strides[0]
    return as_strided(vals[len(c)-1:], shape=out_shp, strides=(-n, n)).copy()


def _toeplitz(c: Array, r: Array) -> Array:
  ncols, = c.shape
  nrows, = r.shape
  if ncols == 0 or nrows == 0:
    return jnp.empty((ncols, nrows), dtype=jnp.promote_types(c.dtype, r.dtype))
  nelems = ncols + nrows - 1
  elems = jnp.concatenate((c[::-1], r[1:]))
  patches = lax.conv_general_dilated_patches(
      elems.reshape((1, nelems, 1)),
      (nrows,), (1,), 'VALID', dimension_numbers=('NTC', 'IOT', 'NTC'),
      precision=lax.Precision.HIGHEST)[0]
  return jnp.flip(patches, axis=0)

