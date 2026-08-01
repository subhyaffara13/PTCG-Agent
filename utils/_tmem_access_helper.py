
def _tmem_access_helper(shape, num) -> tuple[int, str]:
  if num.bit_count() != 1 or num > 128:
    raise ValueError(f"num must be a power of 2 and <= 128, got: {num}")
  match shape:
    case "32x32b":
      num_regs = 1
    case "16x128b":
      num_regs = 2
    case "16x256b":
      num_regs = 4
    case _:
      raise NotImplementedError(f"{shape=} is unsupported")
  num_regs *= num
  if num_regs > 255:
    raise ValueError(
        f"TMEM translation too big : {shape=} and {num=} involve"
        f" {num_regs} registers per-thread, which exceeds the limit of 255"
    )
  regs_vector = ",".join(f"${i}" for i in range(num_regs))
  regs_vector = "{" + regs_vector + "}"
  return num_regs, regs_vector

