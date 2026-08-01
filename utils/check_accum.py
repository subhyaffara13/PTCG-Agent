
def check_accum(aval, acc):
  if not core.typecompat(acc.aval, aval):
    raise ValueError(f"Accumulator aval mismatch: expected {aval}, got {acc.aval}")
  return acc

