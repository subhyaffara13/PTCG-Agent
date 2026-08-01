
def intr_vacopy(dest_list: _ods_ir.Value, src_list: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> VaCopyOp:
  return VaCopyOp(dest_list=dest_list, src_list=src_list, loc=loc, ip=ip)

