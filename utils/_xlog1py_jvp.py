
def _xlog1py_jvp(primals, tangents):
  (x, y) = primals
  (x_dot, y_dot) = tangents
  result = xlog1py(x, y)
  return result, (x_dot * lax.log1p(y) + y_dot * x / (1 + y)).astype(result.dtype)

