
def _scan_sparse(spenv, *spvalues, jaxpr, num_consts, num_carry, **params):
  const_spvalues, carry_spvalues, xs_spvalues = split_list(
    spvalues, [num_consts, num_carry])
  if xs_spvalues:
    # TODO(jakevdp): we don't want to pass xs_spvalues, we want to pass one row
    # of xs spvalues. How to do this?
    raise NotImplementedError("sparse rule for scan with x values.")
  sp_jaxpr, _ = _sparsify_jaxpr(spenv, jaxpr, *const_spvalues, *carry_spvalues, *xs_spvalues)

  consts, _ = tree_flatten(spvalues_to_arrays(spenv, const_spvalues))
  carry, carry_tree = tree_flatten(spvalues_to_arrays(spenv, carry_spvalues))
  xs, xs_tree = tree_flatten(spvalues_to_arrays(spenv, xs_spvalues))

  out = lax.scan_p.bind(*consts, *carry, *xs, jaxpr=sp_jaxpr,
                        num_consts=len(consts), num_carry=len(carry), **params)
  carry_out = tree_unflatten(carry_tree, out[:len(carry)])
  xs_out = tree_unflatten(xs_tree, out[len(carry):])
  return arrays_to_spvalues(spenv, carry_out + xs_out)

