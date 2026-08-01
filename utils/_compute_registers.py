
def _compute_registers(memory_registers: int, num_compute_wgs: int) -> int:
  """Returns the max number of registers to use in compute threads.

  We start with the theoretical max registers per thread if one wargroup
  (128 threads) used the entire SM's 64k register file (64k / 128 = 512).
  Then reserve `memory_registers` for the producer warpgroup and distribute
  the remaining registers evenly among the compute warpgroups.

  Note: The maximum number of registers per thread is 255, so we clamp
  the value.
  """
  n_registers = min(256., (512 - memory_registers) / num_compute_wgs)
  # Round down to the nearest multiple of 8.
  return int((n_registers // 8) * 8)

