
def dot_general_cost_rule(ctx: Context,
                          dimension_numbers: lax.DotDimensionNumbers,
                          **_) -> CostEstimate:
  x_aval, y_aval = ctx.avals_in
  x_shape, y_shape = x_aval.shape, y_aval.shape
  (lhs_contracting_dims, rhs_contracting_dims), (
      lhs_batch_dims, rhs_batch_dims) = dimension_numbers
  assert len(lhs_contracting_dims) == len(rhs_contracting_dims)
  assert len(lhs_batch_dims) == len(rhs_batch_dims)
  flops = 1
  # Flops along a contracting dim is 2*dim (addition and multiplication)
  contracting_flops = 1
  for i in range(len(lhs_contracting_dims)):
    lhs_dim, rhs_dim = lhs_contracting_dims[i], rhs_contracting_dims[i]
    assert x_shape[lhs_dim] == y_shape[rhs_dim]
    contracting_flops *= x_shape[lhs_dim]
  flops *= 2 * contracting_flops
  # Now we handle all other dimensions.
  for i, lhs_dim in enumerate(x_shape):
    if i in lhs_contracting_dims:
      continue
    flops *= lhs_dim
  for i, rhs_dim in enumerate(y_shape):
    if i in rhs_contracting_dims:
      continue
    # Don't double-count batch dims (we already counted for LHS)
    if i in rhs_batch_dims:
      continue
    flops *= rhs_dim
  return CostEstimate(
      flops=flops,
      transcendentals=0,
      bytes_accessed=0,
  )

