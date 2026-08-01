
def intr_stepvector(res: _ods_ir.Type, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return StepVectorOp(res=res, loc=loc, ip=ip).result

