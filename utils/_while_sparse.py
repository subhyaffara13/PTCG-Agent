
def _while_sparse(spenv, *spvalues, cond_jaxpr, cond_nconsts, body_jaxpr, body_nconsts):
  cond_const_spvalues, body_const_spvalues, init_val_spvalues = split_list(
    spvalues, [cond_nconsts, body_nconsts])

  cond_sp_jaxpr, _ = _sparsify_jaxpr(spenv, cond_jaxpr, *cond_const_spvalues, *init_val_spvalues)
  body_sp_jaxpr, out_tree = _sparsify_jaxpr(spenv, body_jaxpr, *body_const_spvalues, *init_val_spvalues)

  cond_consts, _ = tree_flatten(spvalues_to_arrays(spenv, cond_const_spvalues))
  body_consts, _ = tree_flatten(spvalues_to_arrays(spenv, body_const_spvalues))
  init_vals, _ = tree_flatten(spvalues_to_arrays(spenv, init_val_spvalues))

  out_flat = lax.while_p.bind(*cond_consts, *body_consts, *init_vals,
                              cond_nconsts=len(cond_consts), cond_jaxpr=cond_sp_jaxpr,
                              body_nconsts=len(body_consts), body_jaxpr=body_sp_jaxpr)
  return arrays_to_spvalues(spenv, tree_unflatten(out_tree, out_flat))

