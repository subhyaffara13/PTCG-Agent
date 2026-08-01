
def _custom_partitioning_infer_sharding_from_operands(arg_shapes, arg_shardings,
                                                      result_shape,
                                                      backend_string):
  info = _sharding_callbacks[backend_string]
  if result_shape.is_tuple():
    result_shapes = result_shape.tuple_shapes()
  else:
    result_shapes = (result_shape,)
  result_sharding = info.infer_sharding_from_operands(
      *info.static_args,
      info.mesh,
      info.unflatten_arg_shapes(arg_shapes, arg_shardings),
      info.out_tree.unflatten([_to_jax_shape(s) for s in result_shapes]),
  )
  result_shardings = _flatten_sharding(
      info.out_tree, result_sharding, result_shapes)
  return _pack_result_sharding(result_shape, result_shardings)

