
def rcp(in_: _ods_ir.Value[_ods_ir.VectorType], *, rounding: _Optional[_Union[_Any, _ods_ir.Attribute]] = None, approx: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, ftz: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult[_ods_ir.VectorType]:
  return RcpOp(in_=in_, rounding=rounding, approx=approx, ftz=ftz, results=results, loc=loc, ip=ip).result

