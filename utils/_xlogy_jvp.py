
def _xlogy_jvp(primals, tangents):
  (x, y) = primals
  (x_dot, y_dot) = tangents
  result = xlogy(x, y)
  return result, (x_dot * lax.log(y) + y_dot * x / y).astype(result.dtype)

