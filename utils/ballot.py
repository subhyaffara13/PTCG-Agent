
def ballot(result: _ods_ir.Type, predicate: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.IntegerType]:
  return BallotOp(result=result, predicate=predicate, loc=loc, ip=ip).result

