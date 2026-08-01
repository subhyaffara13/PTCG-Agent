
def _with_jit(fn,
              static_argnums=None,
              static_argnames=None,
              device=None,
              backend=None,
              **unused_kwargs):
  """Variant that applies `jax.jit` to fn."""

  return jax.jit(
      fn,
      static_argnums=static_argnums,
      static_argnames=static_argnames,
      device=device,
      backend=backend)

