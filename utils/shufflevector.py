
def shufflevector(res: _ods_ir.Type, v1: _ods_ir.Value[_ods_ir.VectorType], v2: _ods_ir.Value[_ods_ir.VectorType], mask: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return ShuffleVectorOp(res=res, v1=v1, v2=v2, mask=mask, loc=loc, ip=ip).result

