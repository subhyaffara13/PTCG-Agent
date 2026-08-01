
def _mpmd_map_discharge_rule(
    avals_in: Sequence[jax_core.AbstractValue],
    avals_out: Sequence[jax_core.AbstractValue],
    *args: Any,
    jaxprs,
    meshes,
    input_output_aliases,
    debug,
    interpret,
    compiler_params,
    cost_estimate,
    metadata,
    name,
    external_meshes,
    **_,
):
  io_indices = [
      i
      for i, aval in enumerate(avals_in)
      if isinstance(aval, state.AbstractRef)
  ]
  num_in = len(avals_in)
  num_out_orig = len(avals_out)
  num_out_new = len(io_indices)

  new_jaxprs = []
  all_meshes = (*meshes, *external_meshes)

  def _rewrite_to_include_new_outputs(jaxpr):

    def new_body(*args):
      in_refs, orig_out_refs, new_out_refs, scratch_refs = util.split_list(
          args, [num_in, num_out_orig, num_out_new]
      )
      del new_out_refs
      jax_core.eval_jaxpr(
          jaxpr, (), *(in_refs + orig_out_refs + scratch_refs)
      )
      return ()

    all_in_avals = [v.aval for v in jaxpr.invars]
    in_avals_trace, orig_out_avals_trace, scratch_avals_trace = util.split_list(
        all_in_avals, [num_in, num_out_orig]
    )
    new_out_avals_trace = [avals_in[i] for i in io_indices]
    tracing_avals = (
        in_avals_trace
        + orig_out_avals_trace
        + new_out_avals_trace
        + scratch_avals_trace
    )

    debug_info = api_util.debug_info(
        "mpmd_map_discharge", new_body, tracing_avals, {}
    )
    wrapped_fun = lu.wrap_init(new_body, debug_info=debug_info)
    new_jaxpr, _, _ = pe.trace_to_jaxpr_dynamic(wrapped_fun, tracing_avals)
    return new_jaxpr

  for mesh, jaxpr in zip(meshes, jaxprs):
    with mpmd_map_tracing_context(mesh, all_meshes):
      new_jaxprs.append(_rewrite_to_include_new_outputs(jaxpr))

  assert all(
      isinstance(avals_in[i], state.AbstractRef) for i in io_indices
  )
  new_out_avals = [avals_in[i].inner_aval for i in io_indices]  # pyrefly: ignore[missing-attribute]
  updated_out_avals = list(avals_out) + new_out_avals

  new_aliases = dict(input_output_aliases)
  for out_idx, in_idx in enumerate(io_indices):
    new_aliases[in_idx] = num_out_orig + out_idx

  res = mpmd_map_p.bind(
      *args,
      jaxprs=tuple(new_jaxprs),
      meshes=meshes,
      input_output_aliases=FrozenDict(new_aliases),
      out_avals=tuple(updated_out_avals),
      debug=debug,
      interpret=interpret,
      compiler_params=compiler_params,
      cost_estimate=cost_estimate,
      metadata=metadata,
      name=name,
      external_meshes=external_meshes,
  )

  # Split the results into original outputs and updated refs.
  ans, updated_refs = util.split_list(res, [num_out_orig])
  new_invals = [None] * len(avals_in)
  for out_idx, in_idx in enumerate(io_indices):
    new_invals[in_idx] = updated_refs[out_idx]

  return new_invals, ans

