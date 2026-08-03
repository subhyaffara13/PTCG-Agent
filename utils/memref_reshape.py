import math


def memref_reshape(result: _ods_ir.Type, input: _ods_ir.Value[_ods_ir.MemRefType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return MemRefReshapeOp(result=result, input=input, loc=loc, ip=ip).result


def memref_reshape(ref: ir.Value, shape: tuple[int, ...]) -> ir.Value:
  ...


def memref_reshape(ref: MultimemRef, shape: tuple[int, ...]) -> MultimemRef:
  ...


def memref_reshape(
    ref: ir.Value | MultimemRef, shape: tuple[int, ...]
) -> ir.Value | MultimemRef:
  """Reshape by means of folding and unfolding.

  The use of memref fold/unfold may avoid some possible issues with
  strided memrefs.
  """

  if isinstance(ref, MultimemRef):
    return MultimemRef(memref_reshape(ref.ref, shape))

  ref_ty = ir.MemRefType(ref.type)
  if math.prod(ref_ty.shape) != math.prod(shape):
    raise ValueError(
        f"Cannot reshape to a different size. Ref shape: {ref_ty.shape} (size:"
        f" {math.prod(ref_ty.shape)}), new shape: {shape} (size:"
        f" {math.prod(shape)})"
    )
  if not all(dim > 0 for dim in shape):
    raise ValueError(
        "Shapes must havbe only positive dimensions (no -1 or 0 dimensions"
        f" allowed) {shape}"
    )

  src_shape = list(ref_ty.shape)
  dst_shape = list(shape)
  if src_shape == dst_shape:
    return ref
  if not src_shape:
    _, offset = ref_ty.get_strides_and_offset()
    identity = ir.AffineMapAttr.get(ir.AffineMap.get_identity(0))
    if ref_ty.layout == identity:
      new_layout = ir.AffineMapAttr.get(
          ir.AffineMap.get_identity(len(dst_shape))
      )
    else:
      new_layout = ir.StridedLayoutAttr.get(offset, [1] * len(dst_shape))
    result_ty = ir.MemRefType.get(
        dst_shape, ref_ty.element_type, new_layout, ref_ty.memory_space
    )
    return memref.expand_shape(result_ty, ref, [], [], dst_shape)
  if not dst_shape:
    _, offset = ref_ty.get_strides_and_offset()
    identity = ir.AffineMapAttr.get(ir.AffineMap.get_identity(ref_ty.rank))
    contig_strided_1d = ir.Attribute.parse("strided<[1]>")
    if ref_ty.layout == identity or ref_ty.layout == contig_strided_1d:
      new_layout = ir.AffineMapAttr.get(ir.AffineMap.get_identity(0))
    else:
      new_layout = ir.StridedLayoutAttr.get(offset, [])
    result_ty = ir.MemRefType.get(
        (), ref_ty.element_type, new_layout, ref_ty.memory_space
    )
    return memref.collapse_shape(result_ty, ref, [])
  # For contiguous refs we can do arbitrary reshapes easily.
  strides, _ = ref_ty.get_strides_and_offset()
  if all(
      d == 1 or s1 == s2
      for d, s1, s2 in zip(
          ref_ty.shape,
          get_contiguous_strides(ref_ty.shape),
          strides,
          strict=True,
      )
  ):
    return memref_unfold(memref_fold(ref, 0, ref_ty.rank), 0, shape)
  return _reshape(ref, src_shape, dst_shape)

