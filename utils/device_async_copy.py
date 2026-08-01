
def device_async_copy(dst: _ods_ir.Value[_ods_ir.MemRefType], dst_indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], src: _ods_ir.Value[_ods_ir.MemRefType], src_indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], dst_elements: _Union[int, _ods_ir.IntegerAttr], *, src_elements: _Optional[_ods_ir.Value[_ods_ir.IndexType]] = None, bypass_l1: _Optional[bool] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return DeviceAsyncCopyOp(dst=dst, dstIndices=dst_indices, src=src, srcIndices=src_indices, dstElements=dst_elements, srcElements=src_elements, bypassL1=bypass_l1, results=results, loc=loc, ip=ip).result

