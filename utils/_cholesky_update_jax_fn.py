
def _cholesky_update_jax_fn(R, z):
  def _drotg(x, y):
    """Get coefs for Givens rotation in a numerically stable way."""
    def _drotg_nonzero(x, y):
      abs_x = abs(x)
      abs_y = abs(y)
      denominator = lax.select(abs_x > abs_y, abs_x, abs_y)
      x /= denominator
      y /= denominator
      rh = 1 / lax.sqrt(x ** 2 + y ** 2)
      return x * rh, -y * rh
    one_and_zero = (
        np.array(1., dtype=x.dtype),
        np.array(0., dtype=x.dtype),
    )
    return control_flow.cond(
        y == 0, lambda x, y: one_and_zero, _drotg_nonzero, x, y)

  def _drot(
      first_vector: Array, second_vector: Array,
      c_coef: float, s_coef: float) -> tuple[Array, Array]:
    return (
        c_coef * first_vector - s_coef * second_vector,
        c_coef * second_vector + s_coef * first_vector)
  n = z.shape[0]
  for k in range(n):
    c, s = _drotg(R[k, k], z[k])
    row_k, z = _drot(R[k, :], z, c, s)
    R = R.at[k, :].set(row_k)
  return R

