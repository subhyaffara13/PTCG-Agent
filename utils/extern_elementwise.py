
def extern_elementwise(result: _ods_ir.Type, srcs: _Sequence[_ods_ir.Value], libname: _Union[str, _ods_ir.StringAttr], libpath: _Union[str, _ods_ir.StringAttr], symbol: _Union[str, _ods_ir.StringAttr], pure: _Union[bool, _ods_ir.BoolAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ExternElementwiseOp(result=result, srcs=srcs, libname=libname, libpath=libpath, symbol=symbol, pure=pure, loc=loc, ip=ip).result

