
def _mpmd_map_tpu_lowering(
    ctx: mlir.LoweringRuleContext,
    *in_nodes,
    jaxprs,
    meshes,
    input_output_aliases,
    debug,
    interpret,
    compiler_params,
    cost_estimate,
    out_avals,
    metadata,
    name,
    external_meshes,
):
  try:
    from jax._src.pallas.mosaic import pallas_call_registration  # pyrefly: ignore[missing-import]
  except ImportError:
    raise pallas_call._unsupported_lowering_error("tpu")
  num_scratch = len(jaxprs[0].invars) - len(in_nodes) - len(ctx.avals_out)
  return pallas_call_registration.mpmd_map_tpu_lowering_rule(
      ctx,
      *in_nodes,
      jaxprs=jaxprs,
      meshes=meshes,
      input_output_aliases=input_output_aliases,
      debug=debug,
      interpret=interpret,
      compiler_params=compiler_params,
      cost_estimate=cost_estimate,
      out_avals=out_avals,
      metadata=metadata,
      name=name,
      external_meshes=external_meshes,
      num_scratch=num_scratch,
  )

