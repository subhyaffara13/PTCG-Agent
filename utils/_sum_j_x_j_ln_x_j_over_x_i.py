
def _sum_j_x_j_ln_x_j_over_x_i(x):
  r"""Computes \sum_j x_j ln(x_j / x_i)."""
  # By having a = x.reshape([1, -1]) and b = x.reshape([-1, 1]), we can use
  # broadcasting and have:
  # (a / b)[i, j] = x_j / x_i
  # thus giving:
  # \sum_j x_j * log(x_j/ x_i) = sum(a * ln (a/b), axis=1)

  a = x.reshape([1, -1])
  b = x.reshape([-1, 1])

  return np.sum(a * np.log(np.divide(a, b)), axis=1)

