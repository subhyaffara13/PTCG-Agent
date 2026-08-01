
def _pallas_call_jvp_rule(
    primals,
    tangents,
    *,
    jaxpr: jax_core.Jaxpr,
    input_output_aliases: tuple[tuple[int, int], ...],
    grid_mapping: GridMapping,
    mesh: pallas_core.Mesh | None,
    debug: bool,
    interpret: Any,
    compiler_params: CompilerParams | None,
    cost_estimate: CostEstimate | None,
    out_avals: tuple[jax_core.AbstractValue, ...],
    metadata: FrozenDict[str, str] | None,
    name: str | None,
):
  debug_info = jaxpr.debug_info
  if grid_mapping.num_dynamic_grid_bounds:
    raise NotImplementedError("interpret with dynamic grid bounds unsupported")
  if grid_mapping.num_index_operands:
    raise NotImplementedError
  if input_output_aliases:
    raise NotImplementedError("JVP with aliasing not supported.")
  if mesh is not None:
    raise NotImplementedError("pallas_call with a mesh does not support JVP")
  nonzero_tangents = [not isinstance(t, ad_util.Zero) for t in tangents]
  tangents = [t for t in tangents if type(t) is not ad_util.Zero]
  nonzero_tangents_with_outputs = nonzero_tangents + [True] * grid_mapping.num_outputs
  closed_jaxpr = jax_core.ClosedJaxpr(jaxpr, ())
  jvp_jaxpr_, _ = ad.jvp_jaxpr(closed_jaxpr, nonzero_tangents_with_outputs, [])
  jvp_jaxpr, () = jvp_jaxpr_.jaxpr, jvp_jaxpr_.consts  # TODO consts
  # `pallas_call` takes in inputs and returns outputs but its jaxpr *does not*.
  # `pallas_call` takes in a stateful jaxpr, meaning the jaxpr accepts input
  # `Ref`s that are read from followed by output `Ref`s that are written to.
  # This means that when we do `jvp_jaxpr` on the `jaxpr`, we get out a new
  # jaxpr that has tangents following primals. In order for this jaxpr to be
  # compatible w/ `pallas_call` (inputs then outputs), we need to shuffle around
  # the jaxpr's invars.
  primal_refs, primal_out_refs, tangent_refs, tangent_out_refs = split_list(
      jvp_jaxpr.invars, [len(primals), grid_mapping.num_outputs, len(tangents)]
  )
  invars = (*primal_refs, *tangent_refs, *primal_out_refs, *tangent_out_refs)
  jvp_jaxpr = jvp_jaxpr.replace(invars=invars)
  if debug:
    print(f"\nThe jaxpr for the jvp of pallas_call {debug_info.func_src_info}:")
    print(jvp_jaxpr)
  in_bms, out_bms = split_list(grid_mapping.block_mappings, [len(primals)])
  jvp_bms = (*in_bms, *in_bms, *out_bms, *out_bms)
  jvp_grid_mapping = grid_mapping.replace(
      block_mappings=jvp_bms,
      num_inputs=grid_mapping.num_inputs * 2,
      num_outputs=grid_mapping.num_outputs * 2,
  )
  if cost_estimate is not None:
    jvp_cost_estimate = CostEstimate(
        flops=2 * cost_estimate.flops,
        bytes_accessed=2 * cost_estimate.bytes_accessed,
        transcendentals=2 * cost_estimate.transcendentals,
    )
  else:
    jvp_cost_estimate = None
  out_flat = pallas_call_p.bind(
      *primals,
      *tangents,
      jaxpr=jvp_jaxpr,
      grid_mapping=jvp_grid_mapping,
      mesh=mesh,
      interpret=interpret,
      debug=debug,
      input_output_aliases=(),
      compiler_params=compiler_params,
      cost_estimate=jvp_cost_estimate,
      out_avals=(*out_avals, *out_avals),
      metadata=metadata,
      name=name,
  )
  out_primals, out_tangents = split_list(out_flat, [len(out_flat) // 2])
  return out_primals, out_tangents

