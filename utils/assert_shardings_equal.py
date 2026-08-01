
def assert_shardings_equal(x_aval, user_sharding: NamedSharding):
  x_spec = x_aval.sharding.spec
  user_spec = user_sharding.spec._normalized_spec_for_aval(x_aval.ndim)
  if config.remove_size_one_mesh_axis_from_type.value:
    user_spec = remove_size_one_mesh_axis(user_spec, user_sharding.mesh)
  for x, s in zip(x_spec, user_spec):
    if s is PartitionSpec.UNCONSTRAINED:
      continue
    else:
      if x != s:
        raise AssertionError(
            '`with_sharding_constraint` acts as an assert when all axes of'
            f' mesh are of type `Explicit`. The array sharding: {x_spec} did'
            f' not match the sharding provided: {user_spec}. Please use'
            ' `jax.sharding.reshard` to shard your input to the sharding you'
            ' want.')

