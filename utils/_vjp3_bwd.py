
def _vjp3_bwd(in_tree, out_tree, out_known, jaxpr, out_primal_avals, residuals,
              maybe_accums, out_ct):
  cts_flat, out_tree_ = tree_flatten(out_ct, is_leaf=lambda x: isinstance(x, ad.Zero))
  if out_tree != out_tree_:
    _vjp_ct_tree_error(jaxpr, out_tree, out_tree_)
  _vjp_check_ct_avals(cts_flat, out_primal_avals)
  cts_flat = [ct for ct, k in zip(cts_flat, out_known) if not k]
  ad.backward_pass3(jaxpr, True, residuals, maybe_accums, cts_flat)
  arg_cts = [x.freeze() if isinstance(x, ad.ValAccum) else
             DidntWant() if isinstance(x, ad.NullAccum) else GradRef()
             for x in maybe_accums]
  arg_cts = map(ad.instantiate_zeros, arg_cts)
  return tree_unflatten(in_tree, arg_cts)

