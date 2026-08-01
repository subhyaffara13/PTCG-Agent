
def intr_dbg_label(label: _Union[_Any, _ods_ir.Attribute], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DbgLabelOp:
  return DbgLabelOp(label=label, loc=loc, ip=ip)

