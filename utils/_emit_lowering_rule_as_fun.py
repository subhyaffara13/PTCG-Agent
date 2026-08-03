import itertools

def _emit_lowering_rule_as_fun(
    lowering_rule: CachedLoweringRule,
    ctx: ModuleContext,
    eqn_ctx: core.JaxprEqnContext,
    primitive: core.Primitive,
    ordered_effects: Sequence[core.Effect],
    avals_in: Sequence[core.AbstractValue],
    avals_out: Sequence[core.AbstractValue],
    inline: bool,
    **params,
) -> LoweringCacheValue:
  """Emits the contents of a lowering rule as a private function."""
  num_dim_vars = len(ctx.shape_poly_state.dim_vars)
  # TODO(necula) maybe only pass the dim_vars if they are needed?
  dim_var_types = [
      aval_to_ir_type(ctx, core.ShapedArray((), dtypes.default_int_dtype()))
  ] * num_dim_vars

  const_args, const_arg_avals = util.unzip2(core.eqn_params_const_args(params))

  input_types = [_aval_to_ir_types(ctx, a) for a in itertools.chain(const_arg_avals, avals_in)]
  output_types = [_aval_to_ir_types(ctx, a) for a in avals_out]
  token_types = [token_type() for _ in ordered_effects]
  input_types = [*dim_var_types, *token_types, *input_types]
  output_types = [*token_types, *output_types]

  flat_input_types, input_treedef = ir_tree_registry.flatten(input_types)
  flat_output_types, output_treedef = ir_tree_registry.flatten(output_types)
  ftype = ir.FunctionType.get(flat_input_types, flat_output_types)
  if inline:
    func_op = func_dialect.FuncOp(primitive.name, ftype, ip=False)
  else:
    func_op = func_dialect.FuncOp(primitive.name, ftype, ip=ctx.ip)
    func_op.attributes["sym_visibility"] = ir.StringAttr.get("private")
    ctx.symbol_table.insert(func_op).value
  entry_block = func_op.add_entry_block()
  with ir.InsertionPoint(entry_block):
    unflattened_args = input_treedef.unflatten(entry_block.arguments)
    dim_var_values, token_args, const_arg_values, unflattened_args = \
      util.split_list(unflattened_args,
                      [num_dim_vars, len(ordered_effects), len(const_args)])
    const_lowering = {
        (id(c), aval): c_arg
        for c, aval, c_arg in zip(const_args, const_arg_avals, const_arg_values)
    }
    flat_dim_var_values, _ = ir_tree_registry.flatten(dim_var_values)
    sub_ctx = LoweringRuleContext(
        module_context=ctx, primitive=primitive,
        name_stack=source_info_util.new_name_stack(),
        traceback=None,
        avals_in=avals_in, avals_out=avals_out,
        tokens_in=TokenSet(dict(zip(ordered_effects, token_args))),
        tokens_out=None, jaxpr_eqn_ctx=eqn_ctx,
        dim_var_values=flat_dim_var_values,
        const_lowering=const_lowering)
    with source_info_to_location(
      ctx, primitive, source_info_util.new_name_stack(), None
    ):
      outs = lowering_rule(sub_ctx, *unflattened_args, **params)
    if sub_ctx.tokens_out:
      outs = [
          *(sub_ctx.tokens_out.get(eff) for eff in ordered_effects),
          *outs
      ]
    flat_outs, _ = ir_tree_registry.flatten(outs)
    func_dialect.return_(flat_outs)
  return LoweringCacheValue(func_op, flat_output_types, output_treedef,
                            const_args, const_arg_avals, inline)

