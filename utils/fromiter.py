
def fromiter(*args, **kwargs):
  """Unimplemented JAX wrapper for jnp.fromiter.

  This function is left deliberately unimplemented because it may be non-pure and thus
  unsafe for use with JIT and other JAX transformations. Consider using
  ``jnp.asarray(np.fromiter(...))`` instead, although care should be taken if ``np.fromiter``
  is used within jax transformations because of its potential side-effect of consuming the
  iterable object; for more information see `Common Gotchas: Pure Functions
  <https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html#pure-functions>`_.
  """
  raise NotImplementedError(
    "jnp.fromiter() is not implemented because it may be non-pure and thus unsafe for use "
    "with JIT and other JAX transformations. Consider using jnp.asarray(np.fromiter(...)) "
    "instead, although care should be taken if np.fromiter is used within a jax transformations "
    "because of its potential side-effect of consuming the iterable object; for more information see "
    "https://docs.jax.dev/en/latest/notebooks/Common_Gotchas_in_JAX.html#pure-functions")

