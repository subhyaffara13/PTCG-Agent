
def _pow_jvp_rhs(g, ans, x, y):
  y_dtype = dtypes.dtype(y)
  assert dtypes.issubdtype(y_dtype, np.inexact)
  return convert_element_type(mul(g, mul(log(_replace_zero(x)), ans)), y_dtype)

