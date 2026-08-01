
def _shard_map_lowering_shardy(
    ctx: mlir.LoweringRuleContext, in_nodes, jaxpr: core.Jaxpr, mesh, in_specs,
    out_specs, newly_manual_axes, check_vma):
  in_avals_ = [v.aval for v in jaxpr.invars]
  new_axis_context = sharding_impls.SPMDAxisContext(
      _get_spmdaxis_ctx_mesh(mesh), newly_manual_axes | set(mesh.manual_axes))
  sub_ctx = ctx.module_context.replace(axis_context=new_axis_context)

  effects = list(mlir.effects_lib.ordered_effects.filter_in(jaxpr.effects))
  tokens = [ctx.tokens_in.get(eff) for eff in effects]
  num_tokens = len(tokens)
  newly_manual_axes = order_wrt_mesh(mesh, newly_manual_axes)
  if prod([mesh.shape[a] for a in newly_manual_axes]) == 1:
    # No need for a `ManualComputationOp` if all manual axes are size 1.
    with (_extend_axis_env(mesh, set(newly_manual_axes)),
          config._check_vma(check_vma)):
      out_nodes, tokens_out = mlir.jaxpr_subcomp(
          sub_ctx, jaxpr, ctx.name_stack,
          mlir.TokenSet(dict(zip(effects, tokens))),
          (), *in_nodes,
          dim_var_values=ctx.dim_var_values,
          const_lowering=ctx.const_lowering,
          outer_traceback=_jax.Traceback())
      ctx.set_tokens_out(tokens_out)
    return out_nodes

  in_shardings = tuple(
      map(partial(_shardy_shard_map_sharding, ctx, mesh, newly_manual_axes),
          in_specs, ctx.avals_in))
  const_args_and_avals = core.jaxpr_const_args(jaxpr)
  const_args, const_avals = util.unzip2(const_args_and_avals)
  num_const_args = len(const_args)
  const_arg_values, _ = mlir.ir_tree_registry.flatten([
      mlir.ir_constants(c, const_lowering=ctx.const_lowering, aval=aval)
      for c, aval in const_args_and_avals
  ])
  # TODO(necula,yashkatariya): how to construct consts shardy shardings from
  #  consts that can be ndarray or jax.Array?
  const_args_shardings = tuple(
      _shardy_shard_map_sharding(ctx, mesh, newly_manual_axes, P(), core.typeof(c))
      for c in const_args)

  num_dim_vars = len(ctx.dim_var_values)
  in_shardings = (
      (_get_token_sharding(ctx, mesh),) * (num_tokens + num_dim_vars) +
      const_args_shardings + in_shardings)
  in_shardings = sharding_impls.SdyArrayList(in_shardings).build(
      ctx.module_context.sharding_attr_cache)

  out_shardings = tuple(
      map(partial(_shardy_shard_map_sharding, ctx, mesh, newly_manual_axes),
          out_specs, ctx.avals_out))
  out_shardings = (
      _get_token_sharding(ctx, mesh),) * num_tokens + out_shardings
  out_shardings = sharding_impls.SdyArrayList(out_shardings).build(
      ctx.module_context.sharding_attr_cache)

  flat_output_types, _ = mlir.ir_tree_registry.flatten(
      map(partial(mlir._aval_to_ir_types, ctx.module_context), ctx.avals_out))
  output_types = ([hlo.TokenType.get()] * num_tokens + flat_output_types)

  args = (*ctx.dim_var_values, *tokens, *const_arg_values, *in_nodes)
  flat_args, _ = mlir.ir_tree_registry.flatten(args)
  manual_computation_op = sdy.ManualComputationOp(
      output_types, flat_args, in_shardings, out_shardings,
      sdy.ManualAxesAttr.get([ir.StringAttr.get(i) for i in newly_manual_axes]))

  dim_var_types = [
    mlir.aval_to_ir_type(ctx.module_context, core.ShapedArray((), dtypes.default_int_dtype()))
  ] * num_dim_vars
  token_types = [hlo.TokenType.get()] * num_tokens
  const_arg_types, _ = mlir.ir_tree_registry.flatten(
      map(partial(mlir._aval_to_ir_types, ctx.module_context), const_avals))
  in_types, _ = mlir.ir_tree_registry.flatten(
      map(partial(mlir._aval_to_ir_types, ctx.module_context), in_avals_))
  block = ir.Block.create_at_start(
      manual_computation_op.body,
      (*dim_var_types, *token_types, *const_arg_types, *in_types))

  with (ir.InsertionPoint(block), _extend_axis_env(mesh, set(newly_manual_axes)),
        config._check_vma(check_vma)):
    dim_var_values, token_arg_values, const_arg_values, in_args = util.split_list(
        block.arguments, [num_dim_vars, num_tokens, num_const_args])
    out_nodes_, tokens_out = mlir.jaxpr_subcomp(
        sub_ctx, jaxpr, ctx.name_stack,
        mlir.TokenSet(dict(zip(effects, token_arg_values))),
        (), *in_args,
        dim_var_values=dim_var_values,
        const_lowering={
            (id(c), aval): ca
            for c, aval, ca in zip(const_args, const_avals, const_arg_values)
        },
        outer_traceback=_jax.Traceback())
    flat_return_vals, _ = mlir.ir_tree_registry.flatten(
        [*(v for _, v in tokens_out.items()), *out_nodes_]
    )
    sdy.return_(flat_return_vals)
    num_tokens = len(tokens_out.effects())
    tokens_out = ctx.tokens_in.update_tokens(mlir.TokenSet(dict(zip(
        effects, manual_computation_op.results[:num_tokens]))))
    ctx.set_tokens_out(tokens_out)

  return manual_computation_op.results[num_tokens:]

