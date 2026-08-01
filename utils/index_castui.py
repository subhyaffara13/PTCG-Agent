
def index_castui(out: _ods_ir.Type, in_: _ods_ir.Value, *, non_neg: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return IndexCastUIOp(out=out, in_=in_, nonNeg=non_neg, loc=loc, ip=ip).result

