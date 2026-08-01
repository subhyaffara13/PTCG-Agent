
def delay(nanos: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> DelayOp:
  return DelayOp(nanos=nanos, loc=loc, ip=ip)


def delay(nanos: int | jax_typing.Array) -> None:
  """Sleeps for the given number of nanoseconds."""
  delay_p.bind(nanos)

