
def _diag(v: Array, k: int):
  v_shape = np.shape(v)
  if len(v_shape) == 1:
    zero = lambda x: lax.full_like(x, shape=(), fill_value=0)
    n = v_shape[0] + abs(k)
    v = lax.pad(v, zero(v), ((max(0, -k), max(0, k), 0),))
    return where(eye(n, k=k, dtype=bool), v[:, None], zero(v))
  elif len(v_shape) == 2:
    return diagonal(v, offset=k)
  else:
    raise ValueError("diag input must be 1d or 2d")

