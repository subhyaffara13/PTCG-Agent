
def intr_prefetch(addr: _ods_ir.Value, rw: _Union[int, _ods_ir.IntegerAttr], hint: _Union[int, _ods_ir.IntegerAttr], cache: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> Prefetch:
  return Prefetch(addr=addr, rw=rw, hint=hint, cache=cache, loc=loc, ip=ip)

