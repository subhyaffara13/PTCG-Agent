
def match_sync(thread_mask: _ods_ir.Value[_ods_ir.IntegerType], val: _ods_ir.Value, kind: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return MatchSyncOp(thread_mask=thread_mask, val=val, kind=kind, results=results, loc=loc, ip=ip).result

