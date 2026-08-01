
def _iota_lowering_wg(
    ctx: LoweringRuleContext, dtype, shape, dimension, sharding
):
  del ctx, sharding
  result_type = ir.VectorType.get(shape, mgpu_utils.dtype_to_ir_type(dtype))
  return mgpu.dialect.broadcasted_iota(result_type, dimension)

