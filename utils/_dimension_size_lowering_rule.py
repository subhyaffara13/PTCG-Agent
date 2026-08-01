
def _dimension_size_lowering_rule(ctx, arg, *, dimension):
  dim_size = mlir.hlo.get_dimension_size(arg, dimension)
  dim_type = mlir.aval_to_ir_type(ctx.module_context, core.dim_value_aval())
  if dim_size.type != dim_type:
    dim_size = mlir.hlo.convert(dim_type, dim_size)
  return [dim_size]

