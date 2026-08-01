
def _emit_cached_call(
    ctx: ModuleContext,
    eqn: core.JaxprEqn,
    tokens_in: TokenSet,
    dim_var_values: tuple[ir.Value, ...],
    const_lowering: dict[tuple[int, core.AbstractValue], IrValues],
    cache_entry: LoweringCacheValue,
    *args,
) -> tuple[Sequence[IrValues], TokenSet]:
  """Emits a call to an already cached lowering function."""
  const_arg_values = tuple(
      ir_constants(c, const_lowering=const_lowering, aval=aval)
      for c, aval in zip(cache_entry.const_args, cache_entry.const_arg_avals)
  )
  if not eqn.effects:
    ordered_effects = ()
    tokens_in_args = ()
  else:
    ordered_effects = list(effects_lib.ordered_effects.filter_in(eqn.effects))
    tokens_in_args = tuple(tokens_in.get(eff) for eff in ordered_effects)

  flat_args, _ = ir_tree_registry.flatten(
      dim_var_values + tokens_in_args + const_arg_values + args)
  if cache_entry.inline:
    outs = jax_mlir_ext.inlined_func_call(cache_entry.func.operation, flat_args)
  else:
    outs = func_dialect.CallOp(
        cache_entry.flat_output_types,
        ir.FlatSymbolRefAttr.get(cache_entry.func.sym_name.value),
        flat_args
    ).results
  out_nodes = cache_entry.output_treedef.unflatten(outs)

  if not eqn.effects:
    return out_nodes, tokens_in

  token_outs, out_nodes = util.split_list(out_nodes, [len(ordered_effects)])
  return out_nodes, tokens_in.update_tokens(TokenSet(dict(zip(ordered_effects, token_outs))))

