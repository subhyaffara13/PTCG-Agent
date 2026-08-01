
def _shard_map_lowering(ctx: mlir.LoweringRuleContext, *in_nodes,
                        jaxpr: core.Jaxpr, mesh, in_specs, out_specs,
                        check_vma, newly_manual_axes):
  if config.use_shardy_partitioner.value:
    return _shard_map_lowering_shardy(
        ctx, in_nodes, jaxpr, mesh, in_specs, out_specs, newly_manual_axes,
        check_vma)

  in_avals_ = [v.aval for v in jaxpr.invars]
  out_avals_ = [x.aval for x in jaxpr.outvars]
  in_nodes_ = map(partial(_xla_shard, ctx, mesh, newly_manual_axes), in_specs,
                  ctx.avals_in, in_avals_, in_nodes)
  new_axis_context = sharding_impls.SPMDAxisContext(
      _get_spmdaxis_ctx_mesh(mesh), newly_manual_axes | set(mesh.manual_axes))
  sub_ctx = ctx.module_context.replace(axis_context=new_axis_context)
  with _extend_axis_env(mesh, newly_manual_axes), config._check_vma(check_vma):
    out_nodes_, tokens_out = mlir.call_lowering(
        "shmap_body", pe.close_jaxpr(jaxpr), None, sub_ctx, in_avals_,
        out_avals_, ctx.tokens_in, *in_nodes_,
        dim_var_values=ctx.dim_var_values,
        const_lowering=ctx.const_lowering,
        arg_names=map(_pspec_mhlo_attrs, in_specs, in_avals_),
        result_names=map(_pspec_mhlo_attrs, out_specs, out_avals_))
  ctx.set_tokens_out(tokens_out)
  return map(partial(_xla_unshard, ctx, mesh, newly_manual_axes), out_specs,
             out_avals_, ctx.avals_out, out_nodes_)

