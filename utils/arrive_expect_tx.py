
def arrive_expect_tx(barrier: _ods_ir.Value[_ods_ir.MemRefType], expect_tx: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> ArriveExpectTxOp:
  return ArriveExpectTxOp(barrier=barrier, expect_tx=expect_tx, loc=loc, ip=ip)

