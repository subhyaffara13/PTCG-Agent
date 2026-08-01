
def _tridiagonal_solve_jax(dl, d, du, b, *, perturb_singular, **_):
  if perturb_singular:
    raise NotImplementedError("perturb_singular=True is not supported on this platform.")
  impl = _tridiagonal_solve_jax_impl
  for _ in range(dl.ndim - 1):
    impl = api.vmap(impl)
  return impl(dl, d, du, b)

