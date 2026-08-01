
def while_loop_error_check(error, enabled_errors, *in_flat, cond_nconsts,
                           cond_jaxpr, body_nconsts, body_jaxpr):
  if cond_jaxpr.out_avals[0].shape:
    # TODO(lenamartens, sharadmv): support batched while.
    raise ValueError('Checkify does not support batched while-loops '
                     '(checkify-of-vmap-of-while). \nHint: if possible, move '
                     'the vmap to the outer level to get '
                     'vmap-of-checkify-of-while.')

  c_consts, b_consts, carry = split_list(in_flat, [cond_nconsts, body_nconsts])
  # Check if the first cond application will error.
  error, _ = checkify_jaxpr(cond_jaxpr, enabled_errors, error, *c_consts, *carry)

  _, _, error_effects = checkify_while_body_jaxpr(cond_jaxpr, body_jaxpr,
                                                  enabled_errors, error,
                                                  cond_nconsts)
  # merged error!
  error = error._add_placeholder_effects(error_effects)
  err_vals, err_tree = jtu.tree_flatten(error)
  checked_body_jaxpr_, body_out_tree, _ = checkify_while_body_jaxpr(
      cond_jaxpr, body_jaxpr, enabled_errors, error, cond_nconsts)
  num_error_vals = len(err_vals)
  to_move = ([False] * num_error_vals + [True] * cond_nconsts
             + [True] * body_nconsts + [False] * len(carry))
  checked_body_jaxpr = pe.move_binders_to_front(checked_body_jaxpr_, to_move)

  cond_in_flat = [*err_vals, *c_consts, *carry]
  cond_in_flat = map(core.typeof, cond_in_flat)
  checked_cond_jaxpr, _, _ = jaxpr_to_checkify_jaxpr(cond_jaxpr, enabled_errors,
                                                     err_tree, *cond_in_flat)
  compat_cond_jaxpr_ = ignore_error_output_jaxpr(checked_cond_jaxpr, num_error_vals)
  to_move = [False] * num_error_vals + [True] * cond_nconsts + [False] * len(carry)
  compat_cond_jaxpr = pe.move_binders_to_front(compat_cond_jaxpr_, to_move)

  new_in_flat = [*c_consts, *c_consts, *b_consts, *err_vals, *carry]
  all_out_vals = lax.while_p.bind(
      *new_in_flat, cond_nconsts=cond_nconsts, cond_jaxpr=compat_cond_jaxpr,
      body_nconsts=cond_nconsts+body_nconsts, body_jaxpr=checked_body_jaxpr)
  # body_out_tree will have all the metadata of cond because it executes a cond!
  error, out = tree_unflatten(body_out_tree, all_out_vals)
  return error, out

