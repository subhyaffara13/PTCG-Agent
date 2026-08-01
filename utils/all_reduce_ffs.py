
def all_reduce_ffs(x: jax.Array, *, reduce: int = 1) -> jax.Array:
  """Computes the index of the first true element in the array.

  Args:
    x: A 1D array of bools.
    reduce: The factor to reduce the output shape by.

  Returns:
    An array with each element containing the index of the first true element in
    ``x`` or ``x.size`` if there are no true elements.
  """
  return all_reduce_ffs_p.bind(x, reduce=reduce)

