
def memref_unsqueeze(ref: ir.Value, dim) -> ir.Value:
  """Inserts a singleton dimension."""
  ref_ty = ir.MemRefType(ref.type)
  if dim == ref_ty.rank:
    new_shape = list(ref_ty.shape)
    new_shape.append(1)
    identity = ir.AffineMapAttr.get(ir.AffineMap.get_identity(ref_ty.rank))
    if ref_ty.layout == identity:
      new_layout = ir.AffineMapAttr.get(
          ir.AffineMap.get_identity(ref_ty.rank + 1)
      )
    else:
      new_strides, offset = ref_ty.get_strides_and_offset()
      new_strides.append(1)
      new_layout = ir.StridedLayoutAttr.get(offset, new_strides)
    new_ty = ir.MemRefType.get(
        new_shape, ref_ty.element_type, new_layout, ref_ty.memory_space
    )
    assoc = [[d] for d in range(ref_ty.rank)]
    assoc[-1].append(ref_ty.rank)
    return memref.expand_shape(new_ty, ref, assoc, [], new_ty.shape)
  else:
    return memref_unfold(ref, dim, (1, None))

