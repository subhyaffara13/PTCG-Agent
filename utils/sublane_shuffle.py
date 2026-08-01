
def sublane_shuffle(lhs: _ods_ir.Value[_ods_ir.VectorType], rhs: _ods_ir.Value[_ods_ir.VectorType], pattern: _Union[_Sequence[int], _ods_ir.DenseI32ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return SublaneShuffleOp(lhs=lhs, rhs=rhs, pattern=pattern, results=results, loc=loc, ip=ip).result

