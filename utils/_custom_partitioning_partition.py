
def _custom_partitioning_partition(arg_shapes, arg_shardings, result_shape,
                                   result_sharding, backend_string):
  info = _sharding_callbacks[backend_string]
  if result_shape.is_tuple():
    result_shapes = result_shape.tuple_shapes()
    result_shardings = result_sharding.tuple_elements()
  else:
    result_shapes = (result_shape,)
    result_shardings = (result_sharding,)
  mesh, lower_fn, result_sharding, arg_shardings = info.partition(
      *info.static_args,
      info.mesh,
      info.unflatten_arg_shapes(arg_shapes, arg_shardings),
      info.out_tree.unflatten(
          [
              info.unflatten_arg_shape(s, sharding)
              for s, sharding in zip(result_shapes, result_shardings)
          ]
      ),
  )
  module_context = info.module_context

  result_shardings = _flatten_sharding(
      info.out_tree, result_sharding, result_shapes)
  arg_shardings = _flatten_sharding(info.in_tree, arg_shardings, arg_shapes)
  tiled_args = [
      _to_jax_shape(sharding.tile(s))
      for sharding, s in zip(arg_shardings, arg_shapes)
  ]
  tiled_results = [
      _to_jax_shape(sharding.tile(s))
      for sharding, s in zip(result_shardings, result_shapes)
  ]
  closed_jaxpr = api.make_jaxpr(lower_fn, axis_env=list(mesh.shape.items()))(
      *info.in_tree.unflatten(tiled_args)
  )
  if ([(o.shape, o.dtype) for o in closed_jaxpr.out_avals] !=
      [(t.shape, t.dtype) for t in tiled_results]):
    raise ValueError(
        "Mismatch in result shapes. %s vs %s"
        % (repr(closed_jaxpr.out_avals), repr(tiled_results))
    )
  axis_context = sharding_impls.SPMDAxisContext(mesh, frozenset(mesh.axis_names))
  with core.extend_axis_env_nd(mesh.shape.items()):
    module = mlir.build_mlir_module_helper(
        closed_jaxpr,
        name="tmp_xla_computation",
        platforms=module_context.platforms,
        backend=module_context.backend,
        axis_context=axis_context,
    )
  result_sharding = _pack_result_sharding(result_shape, result_shardings)
  return mlir.module_to_bytecode(module), arg_shardings, result_sharding

