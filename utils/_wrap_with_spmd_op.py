
def _wrap_with_spmd_op(name: str,
                       ctx: LoweringRuleContext,
                       x: ir.Value,
                       aval_out: core.AbstractValue,
                       sharding: xc.OpSharding | SdyArray,
                       unspecified_dims: set[int] | None = None,
                       has_side_effect: bool = False,
                       allow_shardy_lowering: bool = False):
  if config.use_shardy_partitioner.value and allow_shardy_lowering:
    return dialects.sdy.sharding_constraint(
        x, sharding.build(ctx.module_context.sharding_attr_cache))  # type: ignore

  # unspecified_dims indicate dimensions whose shardings are not specified and
  # XLA sharding propagation can change them.
  if unspecified_dims:
    backend_config = "unspecified_dims=[" + ",".join(
        [str(i) for i in sorted(unspecified_dims)]) + "]"
  else:
    backend_config = ""
  (result_type,) = aval_to_ir_types(ctx.module_context, aval_out)
  out_shape = core.physical_aval(aval_out).shape  # type: ignore
  if core.is_constant_shape(out_shape):
    result_shapes = None
  else:
    result_shapes = [eval_dynamic_shape_as_tensor(ctx, out_shape)]

  op = custom_call(name, result_types=[result_type], operands=[x],
                   backend_config=backend_config,
                   api_version=1,
                   result_shapes=result_shapes,
                   has_side_effect=has_side_effect)
  set_sharding(ctx.module_context, op, sharding)
  return op.result

