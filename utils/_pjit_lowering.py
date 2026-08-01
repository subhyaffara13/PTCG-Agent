
def _pjit_lowering(ctx: mlir.LoweringRuleContext, *args, name: str,
                   jaxpr: core.ClosedJaxpr, in_shardings,
                   out_shardings, in_layouts, out_layouts, donated_invars,
                   ctx_mesh, keep_unused, inline, compiler_options_kvs):
  mod_ctx = ctx.module_context
  axis_ctx = ctx.module_context.axis_context
  num_devices = None
  if isinstance(axis_ctx, sharding_impls.ShardingContext):
    num_devices = axis_ctx.num_devices
  elif isinstance(axis_ctx, sharding_impls.SPMDAxisContext):
    num_devices = axis_ctx.mesh.size
  key = (jit_p, name, jaxpr, num_devices,
         pxla.SemanticallyEqualShardings(in_shardings, jaxpr.in_avals),
         pxla.SemanticallyEqualShardings(out_shardings, jaxpr.out_avals),
         in_layouts, out_layouts)

  result = mod_ctx.cached_primitive_lowerings.get(key, None)
  if result is None:
    result = _pjit_lower_jaxpr_to_fun(
        ctx, name, jaxpr, in_shardings, out_shardings,
        in_layouts, out_layouts)
    mod_ctx.cached_primitive_lowerings[key] = result

  effects = result.effects
  hoisted_const_values, _ = mlir.ir_tree_registry.flatten([
      mlir.ir_constants(c, const_lowering=ctx.const_lowering, aval=aval)
      for c, aval in result.const_args_and_avals
  ])
  if effects:
    tokens_in = [ctx.tokens_in.get(eff) for eff in effects]
    args = (*ctx.dim_var_values, *tokens_in, *hoisted_const_values, *args)
  else:
    args = (*ctx.dim_var_values, *hoisted_const_values, *args)
  flat_args, _ = mlir.ir_tree_registry.flatten(args)
  with mlir.source_info_to_location(
      ctx.module_context, None,
      ctx.name_stack.extend(result.wrapped_name), ctx.traceback):
    call = func_dialect.CallOp(
        result.flat_output_types, result.symbol_ref, flat_args)
  mlir.wrap_compute_type_in_place(ctx, call.operation)
  out_nodes = result.output_treedef.unflatten(call.results)
  if effects:
    tokens, out_nodes = split_list(out_nodes, [len(effects)])
    tokens_out = ctx.tokens_in.update_tokens(mlir.TokenSet(dict(zip(effects, tokens))))
    ctx.set_tokens_out(tokens_out)
  return out_nodes

