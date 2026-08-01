
def _reduction_lowering(body, ctx: LoweringRuleContext, a, axes):
  flat_args = tree_util.tree_leaves(a)
  (axis,) = axes
  mapped_avals = [jax_core.ShapedArray((), aval.dtype) for aval in ctx.avals_in]
  in_tree = tree_util.tree_structure((a, a))
  flat_fun, out_tree_thunk = api_util.flatten_fun_nokwargs(
      lu.wrap_init(
          body,
          debug_info=api_util.debug_info("pallas triton reduction",
                                         body, (a, a), {})),
      in_tree
  )
  combine_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      flat_fun, [*mapped_avals, *mapped_avals]
  )
  out_tree = out_tree_thunk()
  del out_tree  # Not needed
  if consts:
    raise NotImplementedError("Reductions with constants not supported.")
  element_types = [_element_type(arg.type) for arg in flat_args]
  reduce_op = tt_dialect.ReduceOp(flat_args, axis)
  param_types = element_types * 2
  entry = reduce_op.regions[0].blocks.append(*param_types)
  with ir.InsertionPoint.at_block_begin(entry):
    results = lower_jaxpr_to_triton_ir(
        ctx.context, combine_jaxpr, None, *entry.arguments
    )
    tt_dialect.reduce_return(results)
  reduce_op.verify()
  return list(reduce_op.result)

