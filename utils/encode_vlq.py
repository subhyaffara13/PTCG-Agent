
def encode_vlq(value: int) -> bytes:
  """Encode an integer into a Base-64-VLQ."""
  # Move sign to LSB
  value = ((-value) << 1 | 1) if value < 0 else value << 1
  buf = []

  while True:
    d = value & VLQ_VALUE_MASK
    value >>= VLQ_VALUE_BITWIDTH
    more = value > 0
    if more:
      d |= VLQ_MORE_MASK
    buf.append(VLQ_ALPHABET[d])
    if not more:
      break
  return bytes(buf)

