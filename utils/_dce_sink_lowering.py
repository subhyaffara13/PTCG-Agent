
def _dce_sink_lowering(ctx, x, *, prevent_mlir_dce):
  if not prevent_mlir_dce:
    return []
  rule = ffi.ffi_lowering("dce_sink", has_side_effect=True)
  return rule(ctx, x)

