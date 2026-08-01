
def intr_fake_use(args: _Sequence[_ods_ir.Value], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> FakeUseOp:
  return FakeUseOp(args=args, loc=loc, ip=ip)

