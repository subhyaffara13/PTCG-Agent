
def _pjit_sparse(spenv, *spvalues, jaxpr, in_shardings, out_shardings,
                 in_layouts, out_layouts, donated_invars, ctx_mesh, name,
                 keep_unused, inline, compiler_options_kvs):
  if any(donated_invars):
    raise NotImplementedError("sparse xla_call with donated_invars")

  sp_call_jaxpr, out_tree = _sparsify_jaxpr(spenv, jaxpr, *spvalues)
  args_flat, _ = tree_flatten(spvalues_to_arrays(spenv, spvalues))
  donated_invars = tuple(False for arg in args_flat)

  # TODO(yashkatariya, vanderplas): Flatten twice and set the correct sharding
  # for data and indices.
  in_shardings = in_shardings + tuple(
      sharding_impls.UNSPECIFIED
      for _ in range(len(args_flat) - len(in_shardings))
  )
  out_shardings = out_shardings + tuple(
      sharding_impls.UNSPECIFIED
      for _ in range(len(sp_call_jaxpr.out_avals) - len(out_shardings))
  )
  in_layouts = in_layouts + tuple(
      None for _ in range(len(args_flat) - len(in_layouts))
  )
  out_layouts = out_layouts + tuple(
      None for _ in range(len(sp_call_jaxpr.out_avals) - len(out_layouts))
  )

  out_flat = pjit.jit_p.bind(
      *args_flat,
      jaxpr=sp_call_jaxpr,
      in_shardings=in_shardings,
      out_shardings=out_shardings,
      in_layouts=in_layouts,
      out_layouts=out_layouts,
      donated_invars=donated_invars,
      ctx_mesh=ctx_mesh,
      name=name,
      keep_unused=keep_unused,
      inline=inline,
      compiler_options_kvs=compiler_options_kvs)
  return arrays_to_spvalues(spenv, tree_unflatten(out_tree, out_flat))

