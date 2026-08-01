
def nanosleep(duration: _ods_ir.Value[_ods_ir.IntegerType], *, loc: _Optional[_ods_ir.Location] = None, ip: _Optional[_ods_ir.InsertionPoint] = None) -> NanosleepOp:
  return NanosleepOp(duration=duration, loc=loc, ip=ip)


def nanosleep(nanos: ir.Value):
  """Sleeps the current thread for the given number of nanoseconds."""
  llvm.inline_asm(
      ir.Type.parse("!llvm.void"),
      [nanos],
      "nanosleep.u32 $0;",
      "r",
      has_side_effects=True,
  )

