
def _tpu_custom_call_lowering(
    ctx: mlir.LoweringRuleContext,
    *in_nodes,
    config: CustomCallBackendConfig,
    has_side_effects: TpuSideEffectType,
    kernel_name: str | None,
    out_avals: Any,
    input_output_aliases: tuple[tuple[int, int], ...],
    metadata: Any | None,
) -> ir.OpResultList:
  result_types, _ = mlir.ir_tree_registry.flatten([mlir.aval_to_ir_types(ctx.module_context, aval) for aval in out_avals])
  axis_context = ctx.module_context.axis_context
  if isinstance(axis_context, sharding_impls.SPMDAxisContext):
    manual_axes = axis_context.manual_axes | set(axis_context.mesh.manual_axes)
    if (axis_context.manual_axes and
        manual_axes != frozenset(axis_context.mesh.axis_names)):
      raise NotImplementedError(
          "Mosaic kernels cannot be automatically partitioned. Please wrap the"
          " call in a shard_map."
      )
  elif isinstance(axis_context, sharding_impls.ShardingContext):
    if axis_context.num_devices != 1:
      raise NotImplementedError(
          "Mosaic kernels cannot be automatically partitioned. Please wrap the"
          " call in a shard_map."
      )
  elif config.has_communication:
    raise NotImplementedError(
        "Replica lowering for Mosaic kernels not implemented."
    )
  if all(core.is_constant_shape(aval_out.shape) for aval_out in ctx.avals_out):
    result_shapes = None
  else:
    result_shapes, _ = mlir.ir_tree_registry.flatten([
        mlir.shape_tensor(ctx.module_context, mlir.eval_dynamic_shape(ctx, aval_out.shape))
        for aval_out in ctx.avals_out
    ])
  extra_attributes: dict[str, ir.Attribute] | None = None
  # Add kernel_name and kernel_metadata as attributes to the custom call op.
  # This is because we do not want to pollute the backend_config with this
  # information.
  if kernel_name is not None:
    extra_attributes = dict(kernel_name=ir.StringAttr.get(kernel_name))
  # If the IR version we originally generated the ASM string with is not the
  # same as the one we should have used, we need to downgrade the ASM string.
  ir_version = get_ir_version(ctx)
  if (
      ir_version is not None and
      ir_version != config.lowered_module_asm_version
  ):
    config = config.downgrade_lowered_module_asm(ir_version)
  call = mlir.custom_call(
      "tpu_custom_call",
      result_types=result_types,
      operands=in_nodes,
      backend_config=config.to_json(),
      api_version=1,
      has_side_effect=has_side_effects != TpuSideEffectType.PURE,
      operand_output_aliases=dict(input_output_aliases),
      operand_layouts=_avals_to_layouts(ctx.avals_in),
      result_layouts=_avals_to_layouts(ctx.avals_out),
      result_shapes=result_shapes,
      extra_attributes=extra_attributes,
  )
  metadata_dict: dict[str, ir.Attribute] = {}
  if metadata is not None:
    metadata_dict["kernel_metadata"] = ir.StringAttr.get(
        _compact_json_object(**metadata)
    )
  assert isinstance(has_side_effects, TpuSideEffectType)
  if has_side_effects == TpuSideEffectType.DATAFLOW_SIDE_EFFECTING:
    metadata_dict["xla_allow_dce_side_effecting_op"] = ir.StringAttr.get("true")
  if metadata_dict:
    call.attributes["mhlo.frontend_attributes"] = ir.DictAttr.get(metadata_dict)
  return call.results

