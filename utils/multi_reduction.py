
def multi_reduction(kind: _Union[_Any, _ods_ir.Attribute], source: _ods_ir.Value[_ods_ir.VectorType], acc: _ods_ir.Value, reduction_dims: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return MultiDimReductionOp(kind=kind, source=source, acc=acc, reduction_dims=reduction_dims, results=results, loc=loc, ip=ip).result

