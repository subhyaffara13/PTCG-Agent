
def _pallas_call_to_lojax(
    *hi_args,
    jaxpr: jax_core.Jaxpr,
    input_output_aliases: tuple[tuple[int, int], ...],
    grid_mapping: GridMapping,
    mesh: pallas_core.Mesh | None,
    debug: bool,
    interpret: Any,
    compiler_params: Any,
    cost_estimate: CostEstimate | None,
    out_avals: tuple[jax_core.AbstractValue, ...],
    metadata: FrozenDict[str, str] | None,
    name: str | None,
):
  if any(jax_core.typeof(x).has_qdd for x in hi_args):
    raise NotImplementedError("pallas_call does not support QDD for inputs")
  if any(aval.has_qdd for aval in out_avals):
    raise NotImplementedError("pallas_call does not support QDD for outputs")
  closed_jaxpr = jax_core.ClosedJaxpr(jaxpr, ())
  with grid_mapping.trace_env():
    closed_lo_jaxpr = pe.lower_jaxpr2(closed_jaxpr)
  assert not closed_lo_jaxpr.consts
  lo_jaxpr = closed_lo_jaxpr.jaxpr
  for block_mapping in grid_mapping.block_mappings:
    index_map_jaxpr = block_mapping.index_map_jaxpr
    if index_map_jaxpr.jaxpr.is_high:
      raise NotImplementedError(
          "pallas_call does not support hijax for index_map"
      )
  avals = [jax_core.typeof(a) for a in hi_args]
  lo_args = [lo_val for aval, x in zip(avals, hi_args)
             for lo_val in (aval.read_loval(x) if aval.has_qdd
                            else aval.lower_val(x))]
  lo_out_avals = [
      lo_aval
      for aval in out_avals
      for lo_aval in (aval.lo_ty() if aval.is_high else [aval])
  ]
  lo_grid_mapping = grid_mapping.to_lojax()
  in_avals = [v.aval for v in lo_jaxpr.invars]
  scalar_prefetch_avals = in_avals[lo_grid_mapping.slice_index_ops]
  operand_avals = in_avals[lo_grid_mapping.slice_block_ops]
  scratch_avals = in_avals[lo_grid_mapping.slice_scratch_ops]
  # Some basic checks
  assert len(scalar_prefetch_avals) + len(operand_avals) + len(
      scratch_avals
  ) == len(in_avals)
  assert len(lo_grid_mapping.block_mappings) + len(
      lo_grid_mapping.scratch_avals
  ) + lo_grid_mapping.num_index_operands == len(lo_jaxpr.invars), (
      len(lo_grid_mapping.block_mappings),
      len(lo_grid_mapping.scratch_avals),
      lo_grid_mapping.num_index_operands,
      len(lo_jaxpr.invars),
  )

  # We need to update the input/output aliases to be in terms of the
  # flattened lo inputs/outputs.
  # Get mappings from hi input/outputs to the tuple of lo inputs/outputs
  input_index_mapping = _get_index_mapping(avals)
  output_index_mapping = _get_index_mapping(out_avals)
  new_input_output_aliases = []
  # Alias lo inputs to lo outputs
  for i, o in input_output_aliases:
    assert i in input_index_mapping
    assert o in output_index_mapping
    for i_lo, o_lo in zip(input_index_mapping[i], output_index_mapping[o]):
      new_input_output_aliases.append((i_lo, o_lo))

  lo_outs = pallas_call_p.bind(
      *lo_args,
      jaxpr=lo_jaxpr,
      grid_mapping=lo_grid_mapping,
      mesh=mesh,
      cost_estimate=cost_estimate,
      metadata=metadata,
      compiler_params=compiler_params,
      debug=debug,
      interpret=interpret,
      input_output_aliases=tuple(new_input_output_aliases),
      out_avals=tuple(lo_out_avals),
      name=name,
  )
  return pe.raise_lo_outs(out_avals, lo_outs)

