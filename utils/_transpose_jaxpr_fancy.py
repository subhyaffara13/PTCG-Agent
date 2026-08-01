
def _transpose_jaxpr_fancy(jaxpr, in_tree, in_avals, specs):
  cell = lambda: None
  def transposed(*in_flat):
    primals_ctrefs, cts_in = tree_unflatten(in_tree, in_flat)
    args = ad.unproject_accums(specs, primals_ctrefs)
    ad.backward_pass3(jaxpr.jaxpr, False, jaxpr.consts, args, cts_in)
    cts_out = [x.freeze() if isinstance(x, ad.ValAccum) else None for x in args]
    cts_out, cell.out_tree = tree_flatten(cts_out)  # pyrefly: ignore[missing-attribute]
    return cts_out
  dbg = jaxpr.jaxpr.debug_info.with_unknown_names()
  trans_jaxpr, _, consts = pe.trace_to_jaxpr_dynamic(
      lu.wrap_init(transposed, debug_info=dbg), in_avals)
  return core.ClosedJaxpr(trans_jaxpr, consts), cell.out_tree  # pyrefly: ignore[missing-attribute]


def _transpose_jaxpr_fancy(jaxpr, in_tree, in_avals, specs, inst_out):
  maybe_inst = lambda x, inst: ad.instantiate_zeros(x) if inst else x
  def transposed(*in_flat):
    primals_ctrefs, cts_in = tree_unflatten(in_tree, in_flat)
    args = ad.unproject_accums(specs, primals_ctrefs)
    ad.backward_pass3(jaxpr.jaxpr, False, jaxpr.consts, args, cts_in)
    cts_out = [maybe_inst(x.freeze(), inst) if isinstance(x, ad.ValAccum)
               else None for x, inst in zip(args, inst_out)]
    return cts_out
  dbg = jaxpr.jaxpr.debug_info.with_unknown_names()
  closed_jaxpr, out_avals = pe.trace_to_jaxpr(
      transposed, FlatTree.flatten_args(*in_avals), dbg
  )
  return closed_jaxpr, out_avals.tree

