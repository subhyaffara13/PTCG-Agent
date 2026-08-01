
def strided_store(value_to_store: _ods_ir.Value[_ods_ir.VectorType], base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], strides: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> StridedStoreOp:
  return StridedStoreOp(valueToStore=value_to_store, base=base, indices=indices, strides=strides, loc=loc, ip=ip)

