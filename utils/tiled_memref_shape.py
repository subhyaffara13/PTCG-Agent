
def tiled_memref_shape(ref: ir.Value):
  """Returns the 2D untiled shape and element type of a tiled 4D memref."""
  ref_ty = ir.MemRefType(ref.type)
  if ref_ty.rank != 4:
    raise ValueError(f"Expected a 4D memref, got: {ref_ty}")
  logical_shape = (
      ref_ty.shape[0] * ref_ty.shape[2], ref_ty.shape[1] * ref_ty.shape[3]
  )
  return logical_shape, ref_ty.element_type

