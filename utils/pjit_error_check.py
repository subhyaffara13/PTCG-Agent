
def pjit_error_check(error, enabled_errors, *vals_in, jaxpr,
                     in_shardings, out_shardings,
                     in_layouts, out_layouts,
                     donated_invars, ctx_mesh, name, inline, keep_unused,
                     compiler_options_kvs):
  # jaxpr to checked_jaxpr
  err_vals, err_tree = jtu.tree_flatten(error)
  new_vals_in = [*err_vals, *vals_in]
  in_avals = tuple(map(core.typeof, new_vals_in))
  checked_jaxpr, out_tree, _ = jaxpr_to_checkify_jaxpr(jaxpr, enabled_errors,
                                                       err_tree, *in_avals)

  # Update pjit params to account for extra error values.
  num_error_vals = len(err_vals)
  num_out_error_vals = out_tree.num_leaves - len(out_shardings)
  sharding = sharding_impls.UNSPECIFIED
  new_in_shardings = (*[sharding] * num_error_vals, *in_shardings)
  new_in_layouts = (*[None] * num_error_vals, *in_layouts)
  new_donated_invars = (*[False] * num_error_vals, *donated_invars)

  new_out_shardings = (*[sharding] * num_out_error_vals, *out_shardings)
  new_out_layouts = (*[None] * num_out_error_vals, *out_layouts)

  err_and_out = pjit.jit_p.bind(
      *new_vals_in,
      jaxpr=checked_jaxpr,
      in_shardings=new_in_shardings,
      out_shardings=new_out_shardings,
      in_layouts=new_in_layouts,
      out_layouts=new_out_layouts,
      donated_invars=new_donated_invars,
      ctx_mesh=ctx_mesh,
      name=name,
      inline=inline,
      keep_unused=keep_unused,
      compiler_options_kvs=compiler_options_kvs,
  )
  return tree_unflatten(out_tree, err_and_out)

