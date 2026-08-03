import math


def memref_fold(ref: ir.Value, dim, fold_rank) -> ir.Value:
  ...


def memref_fold(ref: MultimemRef, dim, fold_rank) -> MultimemRef:
  ...


def memref_fold(
    ref: ir.Value | MultimemRef, dim, fold_rank
) -> ir.Value | MultimemRef:
  if isinstance(ref, MultimemRef):
    return MultimemRef(memref_fold(ref.ref, dim, fold_rank))

  ref_ty = ir.MemRefType(ref.type)
  new_shape = list(ref_ty.shape)
  if dim < 0:
    raise ValueError(f"Dimension {dim} is negative")
  if dim + fold_rank > len(new_shape):
    raise ValueError(
        f"Folding {fold_rank} dimensions starting from {dim} is out of bounds"
        f" for shape {new_shape}"
    )
  new_shape[dim : dim + fold_rank] = [
      math.prod(new_shape[dim : dim + fold_rank])
  ]
  identity = ir.AffineMapAttr.get(ir.AffineMap.get_identity(ref_ty.rank))
  contig_strided_1d = ir.Attribute.parse("strided<[1]>")
  # Not sure why but MLIR expects the strided 1D layout to disappear in this op.
  if ref_ty.layout == identity or ref_ty.layout == contig_strided_1d:
    new_layout = ir.AffineMapAttr.get(
        ir.AffineMap.get_identity(ref_ty.rank - fold_rank + 1)
    )
  elif _is_contiguous_shape_slice(ref_ty, slice(dim, dim + fold_rank)):
    new_strides, offset = ref_ty.get_strides_and_offset()
    new_strides[dim : dim + fold_rank] = [new_strides[dim + fold_rank - 1]]
    new_layout = ir.StridedLayoutAttr.get(offset, new_strides)
  else:
    raise ValueError(
        f"strides={ref_ty.get_strides_and_offset()[0]}, {ref_ty.shape=},"
        f" {dim=}, {fold_rank=}"
    )

  new_ty = ir.MemRefType.get(
      new_shape, ref_ty.element_type, new_layout, ref_ty.memory_space
  )
  assoc = [[d] for d in range(dim)]
  assoc.append([dim + i for i in range(fold_rank)])
  assoc.extend([d] for d in range(dim + fold_rank, ref_ty.rank))
  assert len(assoc) == new_ty.rank
  return memref.collapse_shape(new_ty, ref, assoc)

