
def scan_error_check(error, enabled_errors, *in_flat, reverse, length, jaxpr,
                     num_consts, num_carry, unroll):

  consts, carry, xs = split_list(in_flat, [num_consts, num_carry])
  xs_mapped = [core.mapped_aval(length, 0, core.typeof(val)) for val in xs]
  # Query body effects to create a merged error containing all effects (such
  # that in and out carried error are of the same type).
  err_vals, err_tree = jtu.tree_flatten(error)
  new_in_aval = map(core.typeof, [*err_vals, *consts, *carry]) + xs_mapped
  _, _, effects = jaxpr_to_checkify_jaxpr(jaxpr, enabled_errors,
                                          err_tree, *new_in_aval)

  merged_error = error._add_placeholder_effects(effects)
  err_vals, err_tree = jtu.tree_flatten(merged_error)

  # Create checked-jaxpr, with the needed pre-processing on the inputs.
  new_in_aval = map(core.typeof, [*err_vals, *consts, *carry]) + xs_mapped
  checked_jaxpr_, out_tree, _ = jaxpr_to_checkify_jaxpr(jaxpr, enabled_errors,
                                                        err_tree, *new_in_aval)

  tomove = ([False] * len(err_vals) + [True] * len(consts)
            + [False] * (len(carry) + len(xs)))
  checked_jaxpr = pe.move_binders_to_front(checked_jaxpr_, tomove)
  new_in_flat = [*consts, *err_vals, *carry, *xs]
  err_and_out = lax.scan_p.bind(
      *new_in_flat, reverse=reverse, length=length, jaxpr=checked_jaxpr,
      num_consts=len(consts), num_carry=len(carry)+len(err_vals), unroll=unroll)
  err, out = tree_unflatten(out_tree, err_and_out)
  return err, out

