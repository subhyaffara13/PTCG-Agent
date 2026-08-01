
def random_gamma_grad(a: ArrayLike, x: ArrayLike, *, dtype) -> Array:
  r"""Elementwise derivative of samples from `Gamma(a, 1)`."""
  a, x = core.auto_insert_reshard(a, x)
  return random_gamma_grad_impl(a, x, dtype=dtype)

