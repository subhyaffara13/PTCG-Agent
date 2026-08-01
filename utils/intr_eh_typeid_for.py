
def intr_eh_typeid_for(res: _ods_ir.Type, type_info: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return EhTypeidForOp(res=res, type_info=type_info, loc=loc, ip=ip).result

