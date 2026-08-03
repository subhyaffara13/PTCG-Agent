from typing import Any

def get_partition_spec(tree: Any) -> Any:
  """Extracts a PartitionSpec tree from a PyTree containing ``Partitioned`` values."""
  return jax.tree_util.tree_map(
      _get_leaf_pspec, tree, is_leaf=lambda x: isinstance(x, AxisMetadata)
  )


def get_partition_spec(tree: A) -> A:
  """Extracts a PartitionSpec tree from a PyTree containing ``Variable`` values."""

  def f(x):
    if isinstance(x, variablelib.Variable):
      return x.replace(get_var_pspec(x))
    elif hasattr(x, 'shape'):
        return PartitionSpec()
    return None

  return jax.tree.map(
    f, tree, is_leaf=lambda x: isinstance(x, variablelib.Variable)
  )

