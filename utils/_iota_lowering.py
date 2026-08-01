
def _iota_lowering(
    ctx: LoweringRuleContext, dtype, shape, dimension, sharding
):
  del sharding  # Unused.
  if ctx.out_layout_hint is None:
    raise RuntimeError(
        "Failed to infer the output layout of the iota. Please apply"
        " plgpu.layout_cast to its output right after its creation."
    )
  mlir_dtype = mgpu_utils.dtype_to_ir_type(dtype)
  is_signed = mgpu_utils.is_signed(dtype)
  return mgpu.FragmentedArray.broadcasted_iota(
      mlir_dtype, shape, dimension, ctx.out_layout_hint, is_signed=is_signed
  )

