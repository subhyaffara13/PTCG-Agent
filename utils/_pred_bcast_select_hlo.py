
def _pred_bcast_select_hlo(ctx,
    pred_aval: core.ShapedArray, pred: ir.Value, x: mlir.IrValues,
    y: mlir.IrValues, x_y_aval: core.AbstractValue) -> Sequence[ir.Value]:
  if x_y_aval is core.abstract_token:
    flat_x_y, _ = mlir.ir_tree_registry.flatten([x, y])
    return [hlo.after_all(flat_x_y)]
  else:
    assert isinstance(x, ir.Value), x
    assert isinstance(y, ir.Value), y
    assert isinstance(x_y_aval, core.ShapedArray), x_y_aval
    assert x.type == y.type, (x.type, y.type)
    assert (pred_aval.shape == x_y_aval.shape[:len(pred_aval.shape)]), (
            pred_aval.shape, x_y_aval)
    x_y_aval = core.physical_aval(x_y_aval)
    bcast_pred = mlir.broadcast_in_dim(
        ctx, pred, core.ShapedArray(x_y_aval.shape, np.dtype(np.bool_)),
        broadcast_dimensions=list(range(len(pred_aval.shape))))
    return [hlo.select(bcast_pred, x, y)]

