
def _vjp3_callable(spec, out_known, jaxpr, out_primal_avals, in_tree, out_tree,
                   args_res, opaque_res, *maybe_ct_refs):
  if not maybe_ct_refs:
    maybe_ct_refs_flat = [GradValue()] * in_tree.num_leaves
  else:
    maybe_ct_refs_flat, in_tree_ = tree_flatten(maybe_ct_refs)
    if in_tree != in_tree_:
      raise Exception  # TODO accept isomorph tuple tree
  args_res_ = tree_leaves(args_res, is_leaf=lambda x: isinstance(x, NotNeeded))
  residuals = [args_res_[i.idx] if i.primal else opaque_res[i.idx] for i in spec]
  maybe_accums = [check_accum(v.aval.to_ct_aval(), x) if isinstance(x, ad.GradAccum) else
                  ad.RefAccum(v.aval.to_ct_aval(), x) if _is_ref(x) else
                  ad.NullAccum(v.aval.to_ct_aval()) if isinstance(x, DontWant) else
                  ad.ValAccum(v.aval.to_ct_aval())
                  for v, x in zip(jaxpr.invars, maybe_ct_refs_flat)]
  return Partial(partial(_vjp3_bwd, in_tree, out_tree, out_known, jaxpr,
                         out_primal_avals), residuals, maybe_accums)

