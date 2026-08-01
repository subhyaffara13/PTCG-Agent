
def abs_sq(x: jax.typing.ArrayLike) -> jax.Array:
  """Returns the squared absolute value of a (maybe complex) array.

  For real `x`, JAX generates the same HLO from this, `jnp.square(x)`, `x * x`,
  or `x**2`.

  Args:
    x: a (maybe complex) array.

  Returns:
    The squared absolute value of `x`.
  """
  if not isinstance(x, (np.ndarray, jnp.ndarray)):
    raise ValueError(f'`abs_sq` accepts only NDarrays, got: {x}.')
  return (x.conj() * x).real

