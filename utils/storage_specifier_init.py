
def storage_specifier_init(result: _ods_ir.Type, *, source: _Optional[_ods_ir.Value] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return StorageSpecifierInitOp(result=result, source=source, loc=loc, ip=ip).result

