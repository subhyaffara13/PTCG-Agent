
def cp_async_shared_global(dst: _ods_ir.Value, src: _ods_ir.Value, size: _Union[int, _ods_ir.IntegerAttr], modifier: _Union[_Any, _ods_ir.Attribute], *, cp_size: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> CpAsyncOp:
  return CpAsyncOp(dst=dst, src=src, size=size, modifier=modifier, cpSize=cp_size, loc=loc, ip=ip)

