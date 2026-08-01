
def outerproduct(result: _ods_ir.Type, lhs: _ods_ir.Value[_ods_ir.VectorType], rhs: _ods_ir.Value, *, acc: _Optional[_ods_ir.Value[_ods_ir.VectorType]] = None, kind: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return OuterProductOp(result=result, lhs=lhs, rhs=rhs, acc=acc, kind=kind, loc=loc, ip=ip).result

