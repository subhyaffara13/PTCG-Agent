
def _unary_reduce_lower(reducer, unit_factory, ctx, x, *, axes, **kwargs):
  aval_out, = ctx.avals_out
  dtype = aval_out.dtype
  out_type = mlir.aval_to_ir_type(ctx.module_context, aval_out)
  op = hlo.ReduceOp([out_type], [x],
                    [mlir.ir_constant(unit_factory(aval_out.dtype))],
                    mlir.dense_int_array(axes))
  scalar_type = mlir.aval_to_ir_type(ctx.module_context, core.ShapedArray((), dtype))
  reducer_region = op.regions[0].blocks.append(scalar_type, scalar_type)
  with ir.InsertionPoint(reducer_region):
    hlo.return_([reducer(*reducer_region.arguments)])
  return [mlir.lower_with_sharding_in_types(ctx, op.result, aval_out)]

