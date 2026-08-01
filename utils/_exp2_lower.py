
def _exp2_lower(ctx, x, accuracy):
  x_aval, = ctx.avals_in
  log2 = mlir.ir_constant(np.array(np.log(2), x_aval.dtype))
  log2 = mlir.broadcast_in_dim(ctx, log2, x_aval, broadcast_dimensions=())
  return [
      hlo.exponential(
          hlo.multiply(log2, x), result_accuracy=accuracy_attr(accuracy)
      )
  ]

