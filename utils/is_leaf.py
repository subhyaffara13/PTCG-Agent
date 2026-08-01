
def is_leaf(x):
  return (
      isinstance(x, np.ndarray)
      or isinstance(x, jax.sharding.Mesh)
      or isinstance(x, jax.sharding.PartitionSpec)
      or isinstance(x, pytree_checkpoint_handler.ParamInfo)
  )

