
def named_tensor(tensor: _ods_ir.Value, name: _Union[str, _ods_ir.StringAttr], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return NamedTensorOp(tensor=tensor, name=name, results=results, loc=loc, ip=ip).result

