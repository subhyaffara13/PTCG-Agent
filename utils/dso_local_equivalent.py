
def dso_local_equivalent(res: _ods_ir.Type, function_name: _Union[str, _ods_ir.FlatSymbolRefAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return DSOLocalEquivalentOp(res=res, function_name=function_name, loc=loc, ip=ip).result

