
def index_cast(out: _ods_ir.Type, in_: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return IndexCastOp(out=out, in_=in_, loc=loc, ip=ip).result

