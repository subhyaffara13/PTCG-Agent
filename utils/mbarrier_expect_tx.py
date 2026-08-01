
def mbarrier_expect_tx(addr: _ods_ir.Value, txcount: _ods_ir.Value[_ods_ir.IntegerType], *, scope: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> MBarrierExpectTxOp:
  return MBarrierExpectTxOp(addr=addr, txcount=txcount, scope=scope, loc=loc, ip=ip)

