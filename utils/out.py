
def out(tensor: _ods_ir.Value[_ods_ir.RankedTensorType], dest: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> OutOp:
  return OutOp(tensor=tensor, dest=dest, loc=loc, ip=ip)

