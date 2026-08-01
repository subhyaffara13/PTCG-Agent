
def mulf(lhs: _ods_ir.Value, rhs: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, roundingmode: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return MulFOp(lhs=lhs, rhs=rhs, fastmath=fastmath, roundingmode=roundingmode, results=results, loc=loc, ip=ip).result


def mulf(a: ir.Value, b: ir.Value):
  return arith.mulf(a, b, fastmath=arith.FastMathFlags.contract)

