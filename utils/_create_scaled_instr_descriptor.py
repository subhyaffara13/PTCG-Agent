
def _create_scaled_instr_descriptor(
    get_input_encoding: Callable[[ir.Type], int],
    m: int,
    n: int,
    a_type: ir.Type,
    b_type: ir.Type,
    a_scale_idx: int,
    b_scale_idx: int,
    transpose_a: bool,
    transpose_b: bool,
    scale_type: ir.Type,
    sparse: bool = False,
) -> ir.Value:
  desc = 0
  # Bits 0, 1 are reserved
  desc |= sparse << 2  # Sparsity, bit 2
  # Bit 3 is reserved
  assert 0 <= b_scale_idx < 4
  desc |= b_scale_idx << 4  # B scale factor data ID, bits 4-5
  # Bit 6 is reserved
  desc |= get_input_encoding(a_type) << 7  # A dtype, bits 7-9
  desc |= get_input_encoding(b_type) << 10  # B dtype, bits 10-12
  # We ignore negate bits 13-14
  desc |= transpose_a << 15  # Transpose A
  desc |= transpose_b << 16  # Transpose B
  if n % 8 or n > 256:
    raise ValueError(f"N must be a multiple of 8 and <= 256, got: {n}")
  desc |= (n >> 3) << 17  # N, bits 17-22
  if scale_type == ir.Float8E8M0FNUType.get():
    scale_encoding = 1
  elif scale_type == ir.Float8E4M3FNType.get():
    scale_encoding = 0
  else:
    raise NotImplementedError(f"Unsupported scale type: {scale_type}")
  desc |= scale_encoding << 23  # Scale matrix type
  # Bits 24-26 are reserved
  if m % 128 or m > 256:
    raise ValueError(f"M must be a multiple of 16 and <= 256, got: {m}")
  desc |= (m >> 7) << 27  # M >> 7, bits 27-28
  desc |= a_scale_idx << 29  # A scale factor data ID, bits 29-30
  # Bit 31 is reserved
  return arith.constant(ir.IntegerType.get_signless(32), desc)

