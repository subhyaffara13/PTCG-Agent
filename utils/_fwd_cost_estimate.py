
def _fwd_cost_estimate(
    q: jax.Array,
    k: jax.Array,
    v: jax.Array,
    ab: jax.Array | None,
    segment_ids: SegmentIds | None,
    *,
    causal: bool,
    sm_scale: jax.Array | None,
    kernel_inputs_specs,
    kernel_outputs_specs,
) -> pl.CostEstimate | None:
  body_cost = pl.estimate_cost(
    mha_reference,
    q, k, v, ab, segment_ids, causal=causal, sm_scale=sm_scale
  )
  input_bytes = sum(_bytes(x) for x in jax.tree.leaves(kernel_inputs_specs))
  output_bytes = sum(_bytes(x) for x in jax.tree.leaves(kernel_outputs_specs))
  return pl.CostEstimate(
      flops=body_cost.flops,
      transcendentals=body_cost.transcendentals,
      bytes_accessed=input_bytes + output_bytes,
  )

