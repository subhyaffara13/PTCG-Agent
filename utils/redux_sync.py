
def redux_sync(val: _ods_ir.Value, kind: _Union[_Any, _ods_ir.Attribute], mask_and_clamp: _ods_ir.Value[_ods_ir.IntegerType], *, abs: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, nan: _Optional[_Union[bool, _ods_ir.BoolAttr]] = None, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return ReduxOp(val=val, kind=kind, mask_and_clamp=mask_and_clamp, abs=abs, nan=nan, results=results, loc=loc, ip=ip).result

