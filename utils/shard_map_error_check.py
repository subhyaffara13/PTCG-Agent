
def shard_map_error_check(
    error: Error, enabled_errors, *vals_in,
    jaxpr: core.Jaxpr, in_specs, out_specs, **kwargs
):
  if (mesh := kwargs.get('mesh')) is None:
    raise ValueError('Mesh must be provided for shard_map with checkify.')

  err_vals, err_tree = jtu.tree_flatten(error)
  num_error_vals = len(err_vals)
  # Replicated sharding for in errors.
  new_in_specs = (*([P()] * num_error_vals), *in_specs)
  new_vals_in = [*err_vals, *vals_in]
  in_avals = list(map(core.typeof, new_vals_in))
  manual_axes = kwargs.get('newly_manual_axes')
  check_vma = kwargs.get('check_vma')
  for i, v in enumerate(in_avals):
    if not (sharder := core.shard_aval_handlers.get(type(v))):
      raise ValueError(f'Unsupported aval type: {type(v)}')
    in_avals[i] = sharder(mesh, manual_axes, check_vma, new_in_specs[i], v)

  with (jshmap._extend_axis_env(mesh, manual_axes),
        mesh_lib.use_abstract_mesh(jshmap._as_manual_mesh(mesh, manual_axes)),
        config._check_vma(check_vma)):
    # jaxpr to checked_jaxpr
    checked_jaxpr, out_tree, _ = jaxpr_to_checkify_jaxpr(
        pe.close_jaxpr(jaxpr), enabled_errors, err_tree, *in_avals
    )
  num_out_error_vals = out_tree.num_leaves - len(out_specs)

  def expand_errors_leading_dim(*xs):
    outs = core.eval_jaxpr(checked_jaxpr.jaxpr, checked_jaxpr.consts, *xs)
    errs, outs = split_list(outs, [num_out_error_vals])
    errs = [lax.expand_dims(e, [0]) for e in errs]
    return *errs, *outs

  with core.extend_axis_env_nd(mesh.shape.items()), config._check_vma(check_vma):
    checked_jaxpr, _ = pe.trace_to_jaxpr(
        expand_errors_leading_dim,
        FlatTree.flatten((tuple(checked_jaxpr.in_avals), {})),
        debug_info=checked_jaxpr.jaxpr.debug_info)

  # Update shard_map params to account for extra error values.
  # Use fully sharded partitioning for out errors.
  new_out_specs = (*([P(mesh.axis_names)] * num_out_error_vals), *out_specs)
  new_params = dict(
      jaxpr=checked_jaxpr.jaxpr,
      in_specs=new_in_specs,
      out_specs=new_out_specs,
      **kwargs,
  )
  new_params = jshmap.shard_map_p.get_bind_params(new_params)

  err_and_out = jshmap.shard_map_p.bind(
    *new_vals_in, **new_params)
  return tree_unflatten(out_tree, err_and_out)

