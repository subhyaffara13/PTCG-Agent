
def _pad_lower(ctx, x, padding_value, *, padding_config):
  aval_out, = ctx.avals_out
  low, high, interior = util.unzip3(padding_config)
  out = mlir.pad(ctx, aval_out, x, padding_value, low, high, interior)
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

