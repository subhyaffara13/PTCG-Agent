
def vote_sync(mask: _ods_ir.Value[_ods_ir.IntegerType], pred: _ods_ir.Value[_ods_ir.IntegerType], kind: _Union[_Any, _ods_ir.Attribute], *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return VoteSyncOp(mask=mask, pred=pred, kind=kind, results=results, loc=loc, ip=ip).result

