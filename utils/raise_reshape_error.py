
def raise_reshape_error(operand, new_sizes) -> Never:
  raise core.ShardingTypeError(
      'This reshape is not supported. Please specify the sharding of the'
      ' output via the `out_sharding` argument of jax.lax.reshape. Got'
      f' operand type: {operand}, new sizes: {new_sizes}')

