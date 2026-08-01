
def intr_uadd_with_overflow(res: _ods_ir.Type, _gen_arg_0: _ods_ir.Value, _gen_arg_1: _ods_ir.Value, *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return UAddWithOverflowOp(res=res, _gen_arg_0=_gen_arg_0, _gen_arg_1=_gen_arg_1, loc=loc, ip=ip).result

