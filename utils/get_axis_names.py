
def get_axis_names(axes_metadata):
  """Gets axis names for variables as logical PartitionSpecs.

  Args:
    axes_metadata: a single axes-metadata collection from a flax-initialized
      set of collections.

  Returns:
    Collection of Partitionspecs with logical axis names, with the "_axes"
    suffix on variable names removed to match original variable collection for
    annotations.
  """

  def leaf_rewrite(x):
    return None if x is None else jax.sharding.PartitionSpec(*x)

  def rewrite(tree):
    return jax.tree_util.tree_map(leaf_rewrite, tree, is_leaf=_is_logical_spec)

  axes_metadata = unfreeze(axes_metadata)  # pytype: disable=wrong-arg-types
  flat_dict = {
      re.sub(r'_axes$', '', '/'.join(k)): rewrite(v.names)
      for k, v in flatten_dict(axes_metadata).items()
  }
  return freeze(
      unflatten_dict({tuple(k.split('/')): v for k, v in flat_dict.items()})
  )

