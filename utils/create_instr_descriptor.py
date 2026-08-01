
def create_instr_descriptor(
    m: int,
    n: int,
    acc_dtype,
    input_dtype,
    transpose_a: bool = False,
    transpose_b: bool = False,
    sparsity_selector: int | None = None,
) -> ir.Value:
  f16 = ir.F16Type.get()
  f32 = ir.F32Type.get()
  i32 = ir.IntegerType.get_signless(32)

  desc = 0
  if sparsity_selector is not None:
    assert 0 <= sparsity_selector < 3
    desc |= sparsity_selector
    desc |= 1 << 2  # Enable sparsity
  if acc_dtype == f16:
    d_type_val = 0
  elif acc_dtype == f32:
    d_type_val = 1
  elif acc_dtype == i32:
    d_type_val = 2
  else:
    raise NotImplementedError(f"Unsupported accumulator dtype: {acc_dtype}")
  desc |= (d_type_val << 4)  # D type, bits 4-5
  # Bit 6 is reserved
  if input_dtype == f16:
    assert acc_dtype in {f16, f32}
    ab_type_val = 0
  elif input_dtype == ir.BF16Type.get():
    assert acc_dtype == f32
    ab_type_val = 1
  elif input_dtype == ir.Float8E4M3FNType.get():
    assert acc_dtype in {f16, f32}
    ab_type_val = 0
  elif input_dtype == ir.Float8E5M2Type.get():
    assert acc_dtype in {f16, f32}
    ab_type_val = 1
  elif input_dtype == ir.IntegerType.get_signless(8):  # Only s8 for now.
    assert acc_dtype == i32
    ab_type_val = 1
  else:
    raise NotImplementedError(f"Unsupported input dtype: {input_dtype}")
  desc |= (ab_type_val << 7)   # A dtype, bits 7-9
  desc |= (ab_type_val << 10)  # B dtype, bits 10-12
  # We ignore negate bits 13-14
  desc |= transpose_a << 15  # Transpose A
  desc |= transpose_b << 16  # Transpose B
  if n % 8 or n > 256:
    raise ValueError(f"N must be a multiple of 8 and <= 256, got: {n}")
  desc |= (n >> 3) << 17  # N, bits 17-22
  # Bit 23 is reserved
  if m % 16 or m > 256:
    raise ValueError(f"M must be a multiple of 16 and <= 256, got: {m}")
  desc |= (m >> 4) << 24  # M >> 4, bits 24-28
  # Bit 29 is reserved
  # We ignore max shift under .ws, bits 30-31
  return arith.constant(ir.IntegerType.get_signless(32), desc)

