
def _broadcasting_select_hlo(ctx, which, which_aval, x, x_aval, y, y_aval) -> ir.Value:
  """Wrapper around XLA `Select` that broadcasts its arguments."""
  out_shapes = list(lax.broadcast_shapes(
      tuple(which_aval.shape), tuple(x_aval.shape), tuple(y_aval.shape)))
  out_sharding = lax.broadcast_shardings(which_aval, x_aval, y_aval)
  which, x, y = mlir.multi_broadcast_in_dim(ctx, (which, x, y),
                                            (which_aval, x_aval, y_aval),
                                            out_shapes, out_sharding)
  return hlo.select(which, x, y)

