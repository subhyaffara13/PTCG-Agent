
def pmevent(*, masked_event_id: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, event_id: _Optional[_Union[int, _ods_ir.IntegerAttr]] = None, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> PMEventOp:
  return PMEventOp(maskedEventId=masked_event_id, eventId=event_id, loc=loc, ip=ip)

