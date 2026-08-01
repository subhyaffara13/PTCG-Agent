
def intr_experimental_constrained_fdiv(arg_0: _ods_ir.Value, arg_1: _ods_ir.Value, roundingmode: _Union[_Any, _ods_ir.Attribute], fp_exception_behavior: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ConstrainedFDivIntr(arg_0=arg_0, arg_1=arg_1, roundingmode=roundingmode, fpExceptionBehavior=fp_exception_behavior, results=results, loc=loc, ip=ip).result

