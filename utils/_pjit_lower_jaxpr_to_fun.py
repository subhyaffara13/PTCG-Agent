
def _pjit_lower_jaxpr_to_fun(
    ctx: mlir.LoweringRuleContext, name: str, jaxpr: core.ClosedJaxpr,
    in_shardings, out_shardings,
    in_layouts, out_layouts) -> PjitLoweringResult:
  effects = tuple(effects_lib.ordered_effects.filter_in(jaxpr.effects))
  const_args_and_avals = core.jaxpr_const_args(jaxpr.jaxpr)
  const_args, const_arg_avals = util.unzip2(const_args_and_avals)
  in_avals = (*const_arg_avals, *jaxpr.in_avals)
  ca_shardings = const_args_shardings(const_args)
  in_shardings_expanded = ca_shardings + in_shardings
  ca_layouts = const_args_layouts(const_args, const_arg_avals, ca_shardings)
  in_layouts_expanded = ca_layouts + in_layouts

  assert len(in_avals) == len(const_args) + len(jaxpr.in_avals)
  assert len(in_avals) == len(in_shardings_expanded)
  assert len(in_avals) == len(in_layouts_expanded)
  mod_ctx = ctx.module_context
  arg_shardings = [None if isinstance(i, UnspecifiedValue) else i
                   for i in in_shardings_expanded]
  result_shardings = [None if isinstance(o, UnspecifiedValue) else o
                      for o in out_shardings]
  # TODO(b/228598865): non-top-level functions cannot have shardings set
  # directly on the inputs or outputs because they are lost during MLIR->HLO
  # conversion. using_sharding_annotation=False means we add an identity
  # operation instead.
  func = mlir.lower_jaxpr_to_fun(
      mod_ctx, name, jaxpr, effects,
      num_const_args=len(const_args), in_avals=in_avals,
      arg_shardings=arg_shardings, result_shardings=result_shardings,
      use_sharding_annotations=False,
      arg_layouts=in_layouts_expanded, result_layouts=out_layouts)
  output_types = [mlir.aval_to_ir_types(mod_ctx, a) for a in ctx.avals_out]
  output_types = [mlir.token_type()] * len(effects) + output_types
  flat_output_types, output_treedef = mlir.ir_tree_registry.flatten(output_types)
  symbol_ref = ir.FlatSymbolRefAttr.get(func.name.value)
  wrapped_name = util.wrap_name('jit', name)
  return PjitLoweringResult(func, flat_output_types, output_treedef, const_args_and_avals, effects, symbol_ref, wrapped_name)

