
def mlir_addressof(res: _ods_ir.Type, global_name: _Union[str, _ods_ir.FlatSymbolRefAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return AddressOfOp(res=res, global_name=global_name, loc=loc, ip=ip).result

