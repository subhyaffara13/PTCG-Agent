
def intr_experimental_constrained_fpext(res: _ods_ir.Type, arg_0: _ods_ir.Value, fp_exception_behavior: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConstrainedFPExtIntr(res=res, arg_0=arg_0, fpExceptionBehavior=fp_exception_behavior, loc=loc, ip=ip).result

