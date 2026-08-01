
def get_cluster_ref(source: _ods_ir.Value[_ods_ir.MemRefType], *, x: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, y: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, z: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.MemRefType]:
  return GetClusterRefOp(source=source, x=x, y=y, z=z, results=results, loc=loc, ip=ip).result


def get_cluster_ref(
    ref: ir.Value, dim: gpu.Dimension, idx: ir.Value, generic: bool = True
):
  i32 = ir.IntegerType.get_signless(32)
  # We replace the offset in the ref type by 0, because memref_ptr always
  # folds the offset into the pointer.
  ref_ty = ir.MemRefType(ref.type)
  strides, offset = ref_ty.get_strides_and_offset()
  if offset != 0:
    new_layout = ir.StridedLayoutAttr.get(0, strides)
  else:
    new_layout = ref_ty.layout
  result_type = ir.MemRefType.get(
      ref_ty.shape,
      ref_ty.element_type,
      new_layout,
      None if generic else ir.IntegerAttr.get(i32, 7),
  )
  if not is_smem_ref(ref_ty):
    raise ValueError(f"Expected SMEM but got: {ref_ty.memory_space}")
  idxs: list[ir.Value] = [gpu.cluster_block_id(d) for d in gpu.Dimension]
  idxs[dim] = idx
  flat_block = arith.index_cast(i32, cluster_idx(dim_idx=idxs))
  return ptr_as_memref(
      get_cluster_ptr(memref_ptr(ref), flat_block, generic), result_type
  )

