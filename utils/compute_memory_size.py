
def compute_memory_size(values: PyTree) -> int:
  """Computes the total memory size for a sequence of batch requests.

  Args:
    values: Pytree of leaves or values to compute size for.

  Returns:
    Total memory size in bytes.
  """
  leaves = jax.tree.leaves(values)
  return sum(_get_memory_size(v) for v in leaves)

