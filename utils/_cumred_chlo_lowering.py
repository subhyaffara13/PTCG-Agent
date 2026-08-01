
def _cumred_chlo_lowering(ctx, x, *, axis, reverse, reducer, identity):
  dtype = ctx.avals_in[0].dtype
  init_shape = x.type.shape[:axis] + x.type.shape[axis + 1 :]
  init_type = ir.RankedTensorType.get(init_shape, x.type.element_type)

  init = mlir.ir_constant(identity(dtype))
  if init_shape:
    dims = ir.DenseI64ArrayAttr.get([])
    init = hlo.BroadcastInDimOp(init_type, init, dims).result

  scan_op = chlo.ScanOp(
      [x.type],
      [init_type],
      [x],
      [init],
      dimension=ir.IntegerAttr.get(ir.IntegerType.get_signless(64), axis),
      is_reverse=ir.BoolAttr.get(reverse),
      is_associative=ir.BoolAttr.get(True),
  )
  body_block = scan_op.body.blocks.append(init_type, init_type)
  with ir.InsertionPoint(body_block):
    x_arg, carry_arg = body_block.arguments
    res = reducer(x_arg, carry_arg)
    hlo.return_([res, res])
  return scan_op.results[:1]

