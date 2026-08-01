
def _get_sharding_for_varying_out_shape(out_shape, operand, name):
  """Returns a sharding when out_shape may not be the same as operand shape"""
  mesh = operand.sharding.mesh
  for op_sh, out_sh, op_spec in safe_zip(
      operand.shape, out_shape, operand.sharding.spec.partitions):
    if (op_sh != out_sh and op_spec is not None and
        out_sh % _get_sub_spec_size(mesh, op_spec) != 0):
      raise core.ShardingTypeError(
          f"{name} on sharded dims where out dim ({out_sh}) is not divisible by"
          f" mesh axes ({_get_sub_spec_size(mesh, op_spec)}) with spec"
          f" ({op_spec}) is not implemented. Got input"
          f" type={operand.str_short(True)} and output shape={out_shape}")
  # TODO(yashkatariya): Returning operand.sharding as is may or may not move
  # data. So think about how to avoid it which might include creating a new
  # mesh? For example:
  # mesh = {'x': 4}
  # x = jax.device_put(jnp.arange(8), NamedSharding(mesh, P('x')))`
  # ys = lax.split(x, [4, 4])  # This will create outputs of shape (4,)
  # According to the current logic, ys[0].sharding.spec == P('x')
  # which involves data movement.
  return operand.sharding

