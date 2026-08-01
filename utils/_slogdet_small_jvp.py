
def _slogdet_small_jvp(primals, tangents):
  x, = primals
  g, = tangents
  n = x.shape[-1]
  sign, ans = _slogdet_small(x)
  if n == 1:
    ans_dot = g[..., 0, 0] / x[..., 0, 0]
  else:  # n == 2
    x00, x01 = x[..., 0, 0], x[..., 0, 1]
    x10, x11 = x[..., 1, 0], x[..., 1, 1]
    det = (x00 * x11) - (x01 * x10)
    ans_dot = (
        (g[..., 0, 0] * x11 - g[..., 0, 1] * x10
         - g[..., 1, 0] * x01 + g[..., 1, 1] * x00) / det
    )
  if jnp.issubdtype(jnp._dtype(x), np.complexfloating):
    sign_dot = (ans_dot - ufuncs.real(ans_dot).astype(ans_dot.dtype)) * sign
    ans_dot = ufuncs.real(ans_dot)
  else:
    sign_dot = array_creation.zeros_like(sign)
  return (sign, ans), (sign_dot, ans_dot)

