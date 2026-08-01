
def _mlir_to_torch_dtype(torch, mlir_dtype: ir.Type):
  if mlir_dtype == ir.F32Type.get():
    return torch.float32
  if mlir_dtype == ir.F16Type.get():
    return torch.float16
  if mlir_dtype == ir.BF16Type.get():
    return torch.bfloat16
  if isinstance(mlir_dtype, ir.IntegerType):
    int_type = ir.IntegerType(mlir_dtype)
    if int_type.is_signed or int_type.is_signless:
      return getattr(torch, f"int{int_type.width}")
    else:
      return getattr(torch, f"uint{int_type.width}")
  raise NotImplementedError(f"Unsupported MLIR type: {mlir_dtype}")

