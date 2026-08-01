
def _mpmd_map_to_lojax(
    *hi_args,
    meshes,
    jaxprs,
    external_meshes,
    out_avals,
    input_output_aliases,
    compiler_params,
    interpret,
    debug,
    cost_estimate,
    metadata,
    name,
    **params,
):
  in_avals = [jax_core.typeof(a) for a in hi_args]
  if any(aval.has_qdd for aval in in_avals):
    raise NotImplementedError("mpmd_map does not support QDD for inputs")
  if any(aval.has_qdd for aval in out_avals):
    raise NotImplementedError("mpmd_map does not support QDD for outputs")

  lo_args = [
      lo_val
      for aval, x in zip(in_avals, hi_args)
      for lo_val in (aval.read_loval(x) if aval.has_qdd else aval.lower_val(x))
  ]

  lo_out_avals = [lo_aval for aval in out_avals for lo_aval in aval.lo_ty()]

  all_meshes = (*meshes, *external_meshes)
  lo_jaxprs = []
  for mesh, jaxpr in zip(meshes, jaxprs):
    with mpmd_map_tracing_context(mesh, all_meshes):
      closed_jaxpr = jax_core.ClosedJaxpr(jaxpr, ())
      closed_lo_jaxpr = pe.lower_jaxpr2(closed_jaxpr)
      assert not closed_lo_jaxpr.consts
      lo_jaxprs.append(closed_lo_jaxpr.jaxpr)

  input_index_mapping = pallas_call._get_index_mapping(in_avals)
  output_index_mapping = pallas_call._get_index_mapping(out_avals)
  new_input_output_aliases = {}
  for i, o in input_output_aliases.items():
    assert i in input_index_mapping
    assert o in output_index_mapping
    for i_lo, o_lo in zip(input_index_mapping[i], output_index_mapping[o]):
      new_input_output_aliases[i_lo] = o_lo

  lo_outs = mpmd_map_p.bind(
      *lo_args,
      meshes=meshes,
      jaxprs=tuple(lo_jaxprs),
      external_meshes=external_meshes,
      out_avals=tuple(lo_out_avals),
      input_output_aliases=FrozenDict(new_input_output_aliases),
      compiler_params=compiler_params,
      interpret=interpret,
      debug=debug,
      cost_estimate=cost_estimate,
      metadata=metadata,
      name=name,
      **params,
  )
  return pe.raise_lo_outs(out_avals, lo_outs)

