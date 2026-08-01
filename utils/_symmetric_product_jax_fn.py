
def _symmetric_product_jax_fn(a, c, *, alpha, beta):
  a_T = lax.transpose(a, (*range(a.ndim - 2), a.ndim - 1, a.ndim - 2))
  return alpha * lax.batch_matmul(
      a, a_T, precision=lax.Precision.HIGHEST) + beta * c

