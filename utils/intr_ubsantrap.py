
def intr_ubsantrap(failure_kind: _Union[int, _ods_ir.IntegerAttr], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> UBSanTrap:
  return UBSanTrap(failureKind=failure_kind, loc=loc, ip=ip)

