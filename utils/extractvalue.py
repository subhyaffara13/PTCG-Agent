
def extractvalue(res: _ods_ir.Type, container: _ods_ir.Value, position: _Union[_Sequence[int], _ods_ir.DenseI64ArrayAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ExtractValueOp(res=res, container=container, position=position, loc=loc, ip=ip).result

