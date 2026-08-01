
def landingpad(res: _ods_ir.Type, _gen_arg_1: _Sequence[_ods_ir.Value], *, cleanup: _Optional[bool] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return LandingpadOp(res=res, _gen_arg_1=_gen_arg_1, cleanup=cleanup, loc=loc, ip=ip).result

