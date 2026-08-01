
def insert_strided_slice(value_to_store: _ods_ir.Value[_ods_ir.VectorType], dest: _ods_ir.Value[_ods_ir.VectorType], offsets: _Union[_Sequence[int], _ods_ir.ArrayAttr], strides: _Union[_Sequence[int], _ods_ir.ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return InsertStridedSliceOp(valueToStore=value_to_store, dest=dest, offsets=offsets, strides=strides, results=results, loc=loc, ip=ip).result

