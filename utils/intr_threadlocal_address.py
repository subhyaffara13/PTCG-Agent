
def intr_threadlocal_address(res: _ods_ir.Type, global_: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ThreadlocalAddressOp(res=res, global_=global_, loc=loc, ip=ip).result

