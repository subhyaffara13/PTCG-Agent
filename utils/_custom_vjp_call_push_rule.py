
def _custom_vjp_call_push_rule(
    ctx,
    *block_specs,
    call_jaxpr: core.ClosedJaxpr,
    num_consts,
    fwd_jaxpr_thunk,
    bwd,
    out_trees,
    symbolic_zeros,
):
  del ctx, num_consts, fwd_jaxpr_thunk, bwd, out_trees, symbolic_zeros
  return _push_block_spec_jaxpr(call_jaxpr.jaxpr, *block_specs)

