
def unary_cost_rule(transcendental: bool):
  def cost_rule(ctx: Context, **_) -> CostEstimate:
    x_aval, = ctx.avals_in
    new_flops = 0
    new_transcendentals = 0
    if transcendental:
      new_transcendentals += math.prod(x_aval.shape)
    else:
      new_flops += math.prod(x_aval.shape)
    return CostEstimate(
        flops=new_flops,
        transcendentals=new_transcendentals,
        bytes_accessed=0,
    )
  return cost_rule

