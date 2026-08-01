
def all_reduce_population_count(x: jax.Array, *, reduce: int = 1) -> jax.Array:
  """Computes the number of nonzero elements in the array.

  Args:
    x: A 1D array of bools.
    reduce: The factor to reduce the output shape by.

  Returns:
    An array with each element containing the number of true elements in ``x``.
  """
  return all_reduce_population_count_p.bind(x, reduce=reduce)

