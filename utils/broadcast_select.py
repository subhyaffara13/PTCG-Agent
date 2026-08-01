
def broadcast_select(pred: _ods_ir.Value[_ods_ir.RankedTensorType], on_true: _ods_ir.Value, on_false: _ods_ir.Value, *, results: _Optional[_Sequence[_ods_ir.Type]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> _ods_ir.OpResult:
  return BroadcastSelectOp(pred=pred, on_true=on_true, on_false=on_false, results=results, loc=loc, ip=ip).result

