
def _SignedVarintEncoder():
  """Return an encoder for a basic signed varint value (does not include
  tag)."""

  local_int2byte = struct.Struct('>B').pack

  def EncodeSignedVarint(write, value, unused_deterministic=None):
    if value < 0:
      value += (1 << 64)
    bits = value & 0x7f
    value >>= 7
    while value:
      write(local_int2byte(0x80|bits))
      bits = value & 0x7f
      value >>= 7
    return write(local_int2byte(bits))

  return EncodeSignedVarint

