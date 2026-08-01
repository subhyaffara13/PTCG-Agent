
def insertvalue(container: _ods_ir.Value, value: _ods_ir.Value, position: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return InsertValueOp(container=container, value=value, position=position, results=results, loc=loc, ip=ip).result

