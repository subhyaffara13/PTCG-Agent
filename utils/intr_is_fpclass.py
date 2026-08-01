
def intr_is_fpclass(res: _ods_ir.Type, in_: _ods_ir.Value, bit: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return IsFPClass(res=res, in_=in_, bit=bit, loc=loc, ip=ip).result

