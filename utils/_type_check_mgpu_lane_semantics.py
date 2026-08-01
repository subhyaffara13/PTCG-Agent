
def _type_check_mgpu_lane_semantics(v, ty):
  match (ty, v):
    case (RefType(), ir.Value()) if isinstance(v.type, ir.MemRefType):
      pass
    case (ShapeDtypeStruct(), mgpu.FragmentedArray()):
      mlir_dtype = mgpu_utils.dtype_to_ir_type(ty.dtype)
      if v.mlir_dtype != mlir_dtype:
        raise ValueError(
            f"Array dtype mismatch: expected {v.mlir_dtype} got {mlir_dtype}."
        )
      if ty.shape != v.shape:
        raise ValueError(
            f"Array shape mismatch: expected {ty.shape} got {v.shape}."
        )
      if v.layout != ty.layout.to_mgpu():
        raise ValueError(
            f"Array layout mismatch: expected {v.layout} got {ty.layout.to_mgpu()}."
        )
    case (SomeLayout(), mgpu.FragmentedArray()):
      if ty.to_mgpu() != v.layout:
        raise ValueError(f"Unexpected layout for {v} (expected: {ty})")
    case _:
      raise ValueError(f"Unexpected type {ty} for value {v}")

