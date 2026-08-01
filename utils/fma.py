
def fma(a: _ods_ir.Value, b: _ods_ir.Value, c: _ods_ir.Value, *, fastmath: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, roundingmode: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FmaOp(a=a, b=b, c=c, fastmath=fastmath, roundingmode=roundingmode, results=results, loc=loc, ip=ip).result


def fma(a: _ods_ir.Value, b: _ods_ir.Value, c: _ods_ir.Value, rnd: _Union[_Any, _ods_ir.Attribute], *, sat: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, ftz: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, relu: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, oob: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return FmaOp(a=a, b=b, c=c, rnd=rnd, sat=sat, ftz=ftz, relu=relu, oob=oob, results=results, loc=loc, ip=ip).result


def fma(lhs: _ods_ir.Value[_ods_ir.VectorType], rhs: _ods_ir.Value[_ods_ir.VectorType], acc: _ods_ir.Value[_ods_ir.VectorType], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return FMAOp(lhs=lhs, rhs=rhs, acc=acc, results=results, loc=loc, ip=ip).result

