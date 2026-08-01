
def _cond_sparse(spenv, pred, *operands, branches, **params):
  sp_branches, treedefs = zip(*(_sparsify_jaxpr(spenv, jaxpr, *operands)
                                for jaxpr in branches))
  _check_tree_and_avals("sparsified true_fun output",
                        treedefs[0], sp_branches[0].out_avals,
                        "sparsified false_fun output",
                        treedefs[1], sp_branches[1].out_avals)
  args, _ = tree_flatten(spvalues_to_arrays(spenv, (pred, *operands)))
  out_flat = lax.cond_p.bind(*args, branches=tuple(sp_branches), **params)
  out = tree_unflatten(treedefs[0], out_flat)
  return arrays_to_spvalues(spenv, out)

