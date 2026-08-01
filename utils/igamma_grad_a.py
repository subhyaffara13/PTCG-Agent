
def igamma_grad_a(a: ArrayLike, x: ArrayLike) -> Array:
  r"""Elementwise derivative of the regularized incomplete gamma function."""
  a, x = core.auto_insert_reshard(a, x)
  return igamma_grad_a_p.bind(a, x)

