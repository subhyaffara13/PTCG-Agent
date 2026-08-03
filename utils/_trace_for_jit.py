from typing import Callable

def _trace_for_jit(
    fun: Callable, ji: PjitInfo, ctx_mesh: mesh_lib.Mesh,
    dbg: core.DebugInfo, avals, args, kwargs) -> PjitParams:
  args_ft = FlatTree.flatten_static_argnums_argnames(
      args, kwargs, ji.static_argnums, ji.static_argnames)
  avals_ft = args_ft.update(avals)

  has_kwargs = bool(kwargs)
  if has_kwargs and ji.user_specified_in_shardings:
    raise ValueError(
        "pjit does not support kwargs when in_shardings is specified.")

  if not ctx_mesh.empty and (ji.backend or ji.device):
    raise ValueError(
        "Mesh context manager should not be used with jit when backend or "
        "device is also specified as an argument to jit.")

  if (ji.donate_argnums or ji.donate_argnames) and not config.debug_nans.value:
    donated_invars = donation_vector(ji.donate_argnums, ji.donate_argnames,
                                     avals_ft.tree)
  else:
    donated_invars = (False,) * len(avals_ft)

  # If backend or device is set as an arg on jit, then resolve them to
  # in_shardings and out_shardings as if user passed in in_shardings
  # and out_shardings.
  device_or_backend_set = bool(ji.backend or ji.device)
  if device_or_backend_set:
    sharding = _create_sharding_with_device_backend(ji.device, ji.backend)
    leaves, treedef = tree_flatten(sharding)
    in_shardings_leaves = out_shardings_leaves = tuple(leaves)
    in_shardings_treedef = out_shardings_treedef = treedef
  else:
    api_name = 'pjit' if ji.use_resource_env else 'jit'
    in_shardings_leaves = tuple(
        _create_sharding_for_array(ctx_mesh, x, 'in_shardings', api_name)
        for x in ji.in_shardings_leaves)
    out_shardings_leaves = tuple(
        _create_sharding_for_array(ctx_mesh, x, 'out_shardings', api_name)
        for x in ji.out_shardings_leaves)
    in_shardings_treedef = ji.in_shardings_treedef
    out_shardings_treedef = ji.out_shardings_treedef

  assert None not in in_shardings_leaves
  assert None not in out_shardings_leaves

  in_type = avals_ft.map2(
    lambda a, x: core.AvalQDD(a, cur_qdd(x)) if a.has_qdd else a,
    args_ft)
  assert avals_ft is not None

  in_shardings_flat, in_layouts_flat = _process_in_axis_resources(
      in_shardings_treedef, in_shardings_leaves,
      ji.in_layouts_treedef, ji.in_layouts_leaves,
      avals_ft, dbg, device_or_backend_set, has_kwargs)

  qdd_token = _qdd_cache_index(fun, in_type.vals)  # represents qdd state context

  elapsed_time_ctx = (
      dispatch.log_elapsed_time(
          "Finished tracing {fun_name} for jit in {elapsed_time:.9f} sec",
          fun_name(fun), event=dispatch.JAXPR_TRACE_EVENT)
      if core.trace_state_clean() else contextlib.nullcontext())
  with elapsed_time_ctx:
    if ji.use_resource_env:  # pjit
      with (_internal_use_concrete_mesh(ctx_mesh),
            mesh_lib.use_abstract_mesh(ctx_mesh.abstract_mesh)):
        jaxpr, out_avals = pe.trace_to_jaxpr(fun, in_type, dbg, qdd_token)
    else:
      jaxpr, out_avals = pe.trace_to_jaxpr(fun, in_type, dbg, qdd_token)

  if config.debug_key_reuse.value:
    # Import here to avoid circular imports
    from jax.experimental.key_reuse._core import check_key_reuse_jaxpr  # pyrefly: ignore[missing-import]
    check_key_reuse_jaxpr(jaxpr.jaxpr)

  result_paths = tuple(f"result{lu._clean_keystr_arg_names(path)}"
                       for path in out_avals.paths)
  jaxpr.jaxpr._debug_info = jaxpr.debug_info._replace(result_paths=result_paths)

  # TODO(mattjj,yashkatariya): if we take the 'true' path then we *must* fall
  # off the C++ dispatch fast path for correctness. Ensure that happens.
  if any(isinstance(c, core.Tracer) or core.typeof(c).has_qdd for c in jaxpr.consts):
    jaxpr, consts = pe.separate_consts(jaxpr)
  else:
    consts = []

  if config.mutable_array_checks.value:
    _check_no_aliased_closed_over_refs(dbg, (*jaxpr.consts, *consts), args_ft.vals)
  _qdd_cache_update(fun, in_type.vals, qdd_token, consts,
                    jaxpr.in_aval_qdds[:len(consts)])

  out_shardings_flat, out_layouts_flat = _check_and_canonicalize_out_shardings(
      out_shardings_treedef, out_shardings_leaves, ji.out_layouts_treedef,
      ji.out_layouts_leaves, out_avals.tree,
      tuple(out_avals), jaxpr.jaxpr._debug_info, device_or_backend_set)

  assert len(args_ft.vals) == len(in_shardings_flat) == len(in_layouts_flat)

  num_extra_args = len(consts)
  in_shardings_flat = (UNSPECIFIED,) * num_extra_args + in_shardings_flat
  in_layouts_flat = (None,) * num_extra_args + in_layouts_flat
  donated_invars = (False,) * num_extra_args + donated_invars
  assert (len(in_shardings_flat) == len(in_layouts_flat) ==
          len(donated_invars) == len(consts) + len(avals_ft))

  params = dict(
      jaxpr=jaxpr,
      in_shardings=in_shardings_flat,
      out_shardings=out_shardings_flat,
      in_layouts=in_layouts_flat,
      out_layouts=out_layouts_flat,
      donated_invars=donated_invars,
      ctx_mesh=ctx_mesh,
      name=fun_name(fun),
      keep_unused=ji.keep_unused,
      inline=ji.inline,
      compiler_options_kvs=ji.compiler_options_kvs,
  )
  return PjitParams(consts, params, avals_ft.vals, avals_ft.tree_without_statics,
                    out_avals.tree, dbg.safe_arg_names(len(avals_ft)))

