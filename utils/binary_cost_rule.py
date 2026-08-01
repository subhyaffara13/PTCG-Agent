
def binary_cost_rule(ctx: Context, **_) -> CostEstimate:
  aval_out, = ctx.avals_out
  out_flops = math.prod(aval_out.shape)
  return CostEstimate(
      flops=out_flops,
      transcendentals=0,
      bytes_accessed=0,
  )

