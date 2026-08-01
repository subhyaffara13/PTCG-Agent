
def memref_unfold(ref: ir.Value, dim, factors) -> ir.Value:
  """Unfolds dim into two dimensions, the size of leading one given be major_factor."""
  ref_ty = ir.MemRefType(ref.type)
  new_shape = list(ref_ty.shape)
  if sum(f is None for f in factors) > 1:
    raise ValueError("Can only infer one dimension")
  known_factor_prod = np.prod([f for f in factors if f is not None])
  if new_shape[dim] % known_factor_prod:
    raise ValueError("Non-divisible unfold:", new_shape[dim], factors)
  factors = tuple(
      new_shape[dim] // known_factor_prod if f is None else f for f in factors
  )
  new_shape[dim : dim + 1] = factors
  identity = ir.AffineMapAttr.get(ir.AffineMap.get_identity(ref_ty.rank))
  contig_strided_1d = ir.Attribute.parse("strided<[1]>")
  if ref_ty.layout == identity or ref_ty.layout == contig_strided_1d:
    new_layout = ir.AffineMapAttr.get(
        ir.AffineMap.get_identity(ref_ty.rank + len(factors) - 1)
    )
  else:
    new_strides, offset = ref_ty.get_strides_and_offset()
    prev_stride = new_strides[dim]
    inserted_strides = []
    for f in reversed(factors):
      inserted_strides.append(prev_stride)
      prev_stride *= f
    new_strides[dim : dim + 1] = reversed(inserted_strides)
    new_layout = ir.StridedLayoutAttr.get(offset, new_strides)
  new_ty = ir.MemRefType.get(
      new_shape, ref_ty.element_type, new_layout, ref_ty.memory_space
  )
  if dim == ref_ty.rank:
    assoc = [[d] for d in range(ref_ty.rank)]
    assoc[-1].extend(range(ref_ty.rank, ref_ty.rank + len(factors) - 1))
  else:
    assoc = [[d] for d in range(dim)]
    assoc.append(list(range(dim, dim + len(factors))))
    assoc.extend([d + len(factors) - 1] for d in range(dim + 1, ref_ty.rank))
  assert len(assoc) == ref_ty.rank
  return memref.expand_shape(new_ty, ref, assoc, [], new_ty.shape)

