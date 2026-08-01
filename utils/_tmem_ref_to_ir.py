
def _tmem_ref_to_ir(ref: tcgen05.TMEMRef, ty: ir.MemRefType) -> ir.Value:
  """Returns an IR value from a TMEMRef."""
  conversion_cast = builtin.UnrealizedConversionCastOp([ty], [ref.address])
  conversion_cast.attributes["layout"] = layouts_lib.to_layout_attr(ref.layout)
  return conversion_cast.result

