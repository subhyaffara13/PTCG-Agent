
def _size_and_bytes(pytree: Any) -> tuple[int, int]:
  leaves = jax.tree_util.tree_leaves(pytree)
  size = sum(x.size for x in leaves if hasattr(x, 'size'))
  num_bytes = sum(
    x.size * x.dtype.itemsize for x in leaves if hasattr(x, 'size')
  )
  return size, num_bytes


def _size_and_bytes(pytree: tp.Any) -> tuple[int, int]:
  leaves = jax.tree.leaves(pytree)
  size = sum(x.size for x in leaves if hasattr(x, 'size'))
  num_bytes = sum(
    x.size * x.dtype.itemsize for x in leaves if hasattr(x, 'size')
  )
  return size, num_bytes

