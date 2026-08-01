
def arrive(barrier: _ods_ir.Value[_ods_ir.MemRefType], orders_tensor_core: _Union[bool, _ods_ir.BoolAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ArriveOp:
  return ArriveOp(barrier=barrier, orders_tensor_core=orders_tensor_core, loc=loc, ip=ip)

