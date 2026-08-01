
def _T(x: Array) -> Array:
  return lax.transpose(x, (*range(x.ndim - 2), x.ndim - 1, x.ndim - 2))


def _t(key, df, shape, dtype) -> Array:
  if shape is None:
    shape = np.shape(df)
  else:
    _check_shape("t", shape, np.shape(df))

  df = lax.convert_element_type(df, dtype)
  key_n, key_g = _split(key)
  n = normal(key_n, shape, dtype)
  two = lax._const(n, 2)
  half_df = lax.div(df, two)
  g = gamma(key_g, half_df, shape, dtype)
  return n * jnp.sqrt(half_df / g)


def _T(x: Array) -> Array:
  return lax.transpose(x, (*range(x.ndim - 2), x.ndim - 1, x.ndim - 2))

