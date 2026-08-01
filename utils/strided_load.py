
def strided_load(result: _ods_ir.Type, base: _ods_ir.Value[_ods_ir.MemRefType], indices: _Sequence[_ods_ir.Value[_ods_ir.IndexType]], strides: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return StridedLoadOp(result=result, base=base, indices=indices, strides=strides, loc=loc, ip=ip).result

