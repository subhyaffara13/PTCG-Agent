
def _inline_mgpu_lowering_rule_wg_semantics(
    ctx: lowering.LoweringRuleContext,
    *flat_args_and_transforms,
    mgpu_fn: Callable[..., Any],
    flat_arg_types,
    flat_ret_ty,
    pytree_args,
    pytree_ref_transforms,
    pytree_ret_ty,
):
  del pytree_ret_ty
  if ctx.module_ctx.primitive_semantics == gpu_core.PrimitiveSemantics.Warp:
    for r in flat_ret_ty:
      if isinstance(r, ShapeDtypeStruct) and r.shape:
        raise ValueError(
            "inline_mgpu in a single-warp context only supports scalar return"
            f" types. Got shape={r.shape}."
        )

  flat_transformed_args = _inline_mgpu_flat_transformed_args(
      ctx,
      flat_args_and_transforms,
      flat_arg_types,
      pytree_args,
      pytree_ref_transforms,
  )

  in_types, in_layouts, in_transforms = (
      _custom_primitive_in_specs(
          ctx, flat_arg_types, flat_transformed_args, pytree_args
      )
  )
  results_ty, out_layouts = _custom_primitive_op_results(flat_ret_ty)

  custom_op = mgpu.dialect.CustomPrimitiveOp(
      result=results_ty,
      operands_=flat_transformed_args,  # pyrefly: ignore[bad-argument-type]
      in_layouts=in_layouts,
      in_transforms=in_transforms,
      out_layouts=[l for l in out_layouts if l is not None],
  )
  block: ir.Block = custom_op.body.blocks.append(*in_types)
  _populate_custom_primitive_op_block(
      ctx,
      block,
      mgpu_fn,
      pytree_args,
      in_layouts,
      in_transforms,
      results_ty,
      out_layouts,
  )

  # We need to ensure that the block doesn't capture any values from the context
  # and uses args for everything instead. E.g. `LaunchContext.tma_descriptors`
  # will be captured when calling `ctx.async_copy`.
  custom_op = lowering._isolate_from_above(custom_op)

  return custom_op.results

