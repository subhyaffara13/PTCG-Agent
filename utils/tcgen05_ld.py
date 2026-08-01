
def tcgen05_ld(res: _ods_ir.Type, shape: _Union[_Any, _ods_ir.Attribute], tmem_addr: _ods_ir.Value, *, pack: _Optional[bool] = None, offset: _Optional[_ods_ir.Value[_ods_ir.IntegerType]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return Tcgen05LdOp(res=res, shape=shape, tmemAddr=tmem_addr, pack=pack, offset=offset, loc=loc, ip=ip).result

