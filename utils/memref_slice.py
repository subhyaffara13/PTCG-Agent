
def memref_slice(result: _ods_ir.Type, mem_ref: _ods_ir.Value[_ods_ir.MemRefType], base_idx: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], dynamic_sizes: _Sequence[_ods_ir.Value[_ods_ir.IntegerType]], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return MemRefSliceOp(result=result, mem_ref=mem_ref, base_idx=base_idx, dynamic_sizes=dynamic_sizes, loc=loc, ip=ip).result


def memref_slice(ref: ir.Value[ir.MemRefType], index) -> ir.Value:
  ref_ty = ir.MemRefType(ref.type)
  base_indices, slice_shape, is_squeezed = parse_indices(index, ref_ty.shape)
  # TODO(apaszke): Check that slice is within the memref (indices might be
  # dynamic, but we can at least catch some OOB slices).

  memref_strides, offset = ref_ty.get_strides_and_offset()
  dynamic_offset = ir.ShapedType.get_dynamic_stride_or_offset()
  new_offset = offset
  if new_offset != dynamic_offset:
    for idx, stride in zip(base_indices, memref_strides):
      if isinstance(idx, int):
        new_offset += idx * stride
      else:
        new_offset = dynamic_offset
        break
  new_strides = [
      s for s, squeeze in zip(memref_strides, is_squeezed) if not squeeze
  ]
  new_shape = [s for s, squeeze in zip(slice_shape, is_squeezed) if not squeeze]
  new_layout = ir.StridedLayoutAttr.get(new_offset, new_strides)

  ref_slice = memref.subview(
      ref,
      base_indices,
      slice_shape,
      [1] * len(ref_ty.shape),
      result_type=ir.MemRefType.get(
          new_shape, ref_ty.element_type, new_layout, ref_ty.memory_space
      ),
  )
  return ref_slice

