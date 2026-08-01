
def _is_axis_spec(x):
  return (
      isinstance(x, str)
      or x is jax.sharding.PartitionSpec.UNCONSTRAINED
      or x is None
  )

