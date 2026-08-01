
def tree_memory_per_device(tree: tuple[jax.Array, ...] | jax.Array) -> int:
  """Returns the memory usage of a PyTree on each device (in bytes)."""
  leaf_memory_per_device = jax.tree_util.tree_map(
      get_leaf_memory_per_device, tree
  )
  return jax.tree.reduce(lambda x, y: x + y, leaf_memory_per_device)

