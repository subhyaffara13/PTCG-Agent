
def _custom_partitioning_lowering_rule(ctx: mlir.LoweringRuleContext, *values,
                                       call, in_tree, out_tree,
                                       propagate_user_sharding, partition,
                                       infer_sharding_from_operands,
                                       decode_shardings,
                                       sharding_rule,
                                       static_args):
  axis_context = ctx.module_context.axis_context
  if (isinstance(axis_context, sharding_impls.SPMDAxisContext) and
      set(axis_context.manual_axes) == set(axis_context.mesh.axis_names)):
    return mlir.lower_fun(core.jaxpr_as_fun(call), multiple_results=True)(ctx, *values)

  mesh = mesh_lib.thread_resources.env.physical_mesh
  if isinstance(axis_context, sharding_impls.ShardingContext):
    devices = axis_context.device_assignment
    if devices is None:
      raise AssertionError(
          'Please file a bug at https://github.com/jax-ml/jax/issues')
    am = axis_context.abstract_mesh
    if am is not None:
      mesh = mesh_lib.Mesh(np.array(devices).reshape(am.axis_sizes),
                           am.axis_names)
  elif isinstance(axis_context, sharding_impls.SPMDAxisContext):
    devices = axis_context.mesh._flat_devices_tuple
  else:
    devices = None

  if not devices or len(devices) == 1:
    return mlir.lower_fun(
        core.jaxpr_as_fun(call), multiple_results=True)(ctx, *values)

  def to_mesh_pspec_sharding(hlo_sharding: xc.HloSharding | None, ndim):
    if hlo_sharding is None:
      return hlo_sharding
    if mesh.empty or not decode_shardings:
      assert devices is not None
      return sharding_impls.GSPMDSharding(devices, hlo_sharding)
    pspec = sharding_impls.parse_flatten_op_sharding(
        hlo_sharding, mesh)[0]
    pspec = sharding_impls.PartitionSpec(*pspec, *((None,) * (ndim - len(pspec))))
    return sharding_impls.NamedSharding(mesh, pspec)

  sharding_callback_info = _ShardingCallbackInfo(propagate_user_sharding,
      partition, to_mesh_pspec_sharding, in_tree, out_tree,
      infer_sharding_from_operands, ctx.module_context, mesh, static_args)
  key = str(id(sharding_callback_info))
  _sharding_callbacks[bytes(key, 'utf8')] = sharding_callback_info
  # We need to make sure `sharding_callback_info` is still alive when the SPMD
  # partitioner runs so we keep it alive by attaching it to the executable.
  ctx.module_context.add_keepalive(sharding_callback_info)

  result_types, _ = mlir.ir_tree_registry.flatten(
      [mlir.aval_to_ir_types(ctx.module_context, a) for a in call.out_avals])
  out = hlo.CustomCallOp(
      result_types,
      list(values),
      call_target_name=ir.StringAttr.get(_CUSTOM_PARTITIONING_CALL_NAME),
      has_side_effect=ir.BoolAttr.get(False),
      api_version=mlir.i32_attr(2),
      called_computations=ir.ArrayAttr.get([]),
      backend_config=ir.StringAttr.get(key),
      operand_layouts=None,
      result_layouts=None)
  if sharding_rule is not None:
    value_types, _ = mlir.ir_tree_registry.flatten(
        [mlir.aval_to_ir_types(ctx.module_context, a) for a in call.in_avals])
    if callable(sharding_rule):
      sharding_rule = sharding_rule(*static_args, mesh, value_types, result_types)
      if isinstance(sharding_rule, (list, tuple)) and len(sharding_rule) == 2:
        sharding_rule, sharding_rule_dict = sharding_rule
      else:
        sharding_rule_dict = {}
      if isinstance(sharding_rule, str):
        sharding_rule = str_to_sdy_sharding_rule(sharding_rule, **sharding_rule_dict)
      elif not isinstance(sharding_rule, SdyShardingRule):
          raise ValueError("sharding_rule callable must produce either an "
                           "SdyShardingRule object or an Einsum-like notation "
                           "string.")
    out.attributes['sdy.sharding_rule'] = sdy_sharding_rule_to_mlir(
      sharding_rule, value_types, result_types)
  return out.results

