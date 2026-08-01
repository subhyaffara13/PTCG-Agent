
def _associative_scan_lowering(body, ctx: LoweringRuleContext, args, axes):
  flat_args = tree_util.tree_leaves(args)
  (axis,) = axes
  dtype = ctx.avals_in[0].dtype
  in_avals = [
      jax_core.ShapedArray((), dtype=dtype),
      jax_core.ShapedArray((), dtype=dtype),
  ]
  in_tree = tree_util.tree_structure((args, args))
  flat_fun, out_tree_thunk = api_util.flatten_fun_nokwargs(
      lu.wrap_init(
          body,
          debug_info=api_util.debug_info("pallas triton associative_scan",
                                         body, (args, args), {})),
      in_tree
  )
  combine_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      flat_fun, in_avals
  )
  out_tree = out_tree_thunk()
  del out_tree  # Not needed
  if consts:
    raise NotImplementedError("Associative scan with constants not supported.")
  element_types = [_element_type(arg.type) for arg in flat_args]
  scan_op = tt_dialect.ScanOp(flat_args, axis)
  param_types = element_types * 2
  entry = scan_op.regions[0].blocks.append(*param_types)
  with ir.InsertionPoint.at_block_begin(entry):
    results = lower_jaxpr_to_triton_ir(
        ctx.context, combine_jaxpr, None, *entry.arguments
    )
    tt_dialect.scan_return(results)
  scan_op.verify()
  return list(scan_op.result)

