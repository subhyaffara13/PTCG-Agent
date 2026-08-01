
def _nary_lower_hlo(
    op: Callable, ctx, *args: ir.Value, accuracy=None, **params
) -> Sequence[ir.Value]:
  """Lowers an elementwise operator to its MLIR equivalent.
  """
  out_dtype = params.pop('out_dtype', None)
  del params
  avals_in, (aval_out,) = ctx.avals_in, ctx.avals_out
  args = tuple(mlir.multi_broadcast_in_dim(ctx, args, avals_in, aval_out.shape,
                                           aval_out.sharding))

  if out_dtype is not None:
    ir_type = mlir.aval_to_ir_type(ctx.module_context, aval_out)
    args = tuple(hlo.convert(ir_type, a) for a in args)

  out = op(*args)
  if accuracy:
    out = op(*args, result_accuracy=accuracy_attr(accuracy))
  return [mlir.lower_with_sharding_in_types(ctx, out, aval_out)]

