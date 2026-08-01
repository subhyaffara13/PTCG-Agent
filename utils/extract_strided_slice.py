
def extract_strided_slice(result: _ods_ir.Type, source: _ods_ir.Value[_ods_ir.VectorType], offsets: _Union[_Sequence[int], _ods_ir.ArrayAttr], sizes: _Union[_Sequence[int], _ods_ir.ArrayAttr], strides: _Union[_Sequence[int], _ods_ir.ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ExtractStridedSliceOp(result=result, source=source, offsets=offsets, sizes=sizes, strides=strides, loc=loc, ip=ip).result

