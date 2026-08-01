
def _integer_pow_cost_rule(ctx: Context, *, y: int) -> CostEstimate:
  x_aval, = ctx.avals_in
  num_elements = math.prod(x_aval.shape)
  if y == 0 or y == 1:
    # No flops, the result is 0 or a copy of the input.
    cost_per_element = 0
  else:
    # We assume integer pow is implemented using repeated squaring.
    # The cost is log(y) squarings, plus one multiply per non-zero bit.
    highest_bit = math.floor(math.log(y, 2))
    cost_per_element = highest_bit + y.bit_count()
  return CostEstimate(
      flops=num_elements * cost_per_element,
      transcendentals=0,
      bytes_accessed=0,
  )

