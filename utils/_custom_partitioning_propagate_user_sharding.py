
def _custom_partitioning_propagate_user_sharding(user_sharding, shape,
                                                 backend_string):
  info = _sharding_callbacks[backend_string]
  if info.propagate_user_sharding is None:
    return user_sharding
  if shape.is_tuple():
    user_shapes = shape.tuple_shapes()
    user_shardings = user_sharding.tuple_elements()
  else:
    user_shapes = (shape,)
    user_shardings = (user_sharding,)
  user_shape = info.out_tree.unflatten(
      [
          info.unflatten_arg_shape(s, sharding)
          for s, sharding in zip(user_shapes, user_shardings)
      ]
  )
  result_sharding = info.propagate_user_sharding(
      *info.static_args, info.mesh, user_shape
  )
  result_shardings = _flatten_sharding(
      info.out_tree, result_sharding, user_shapes)
  return _pack_result_sharding(shape, result_shardings)

