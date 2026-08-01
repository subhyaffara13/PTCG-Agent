
def diff_debug(new_dbg, old_dbg) -> tuple[int, int, str] | None:
  msg = "Debug info doesn't match."
  num_diff = sum(map(op.ne, new_dbg, old_dbg))
  if num_diff: return 2, num_diff, msg

