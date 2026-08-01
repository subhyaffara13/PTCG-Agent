
def _reduce_precision_lower(ctx, operand, *, exponent_bits, mantissa_bits):
  aval_out, = ctx.avals_out
  out = hlo.reduce_precision(operand, mlir.i32_attr(exponent_bits),
                             mlir.i32_attr(mantissa_bits))
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

