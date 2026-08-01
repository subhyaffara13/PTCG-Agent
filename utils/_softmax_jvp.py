
def _softmax_jvp(axis, primals, tangents):
  (x, where, initial), (x_dot, _, _) = primals, tangents
  y = _softmax(x, axis, where, initial)
  return y, y * (x_dot - (y * x_dot).sum(axis, where=where, keepdims=True))

