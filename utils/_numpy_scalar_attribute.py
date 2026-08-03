from typing import Any

def _numpy_scalar_attribute(val: Any) -> ir.Attribute:
  mlir_type = dtype_to_ir_type(val.dtype)
  if isinstance(mlir_type, ir.IntegerType):
    return ir.IntegerAttr.get(mlir_type, val)
  elif isinstance(mlir_type, ir.FloatType):
    return ir.FloatAttr.get(mlir_type, val)
  else:
    raise TypeError(f"Unsupported scalar attribute type: {type(val)}")

