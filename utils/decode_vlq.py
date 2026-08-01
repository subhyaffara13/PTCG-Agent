
def decode_vlq(enc: Iterable[int]) -> int:
  """Decode a Base-64-VLQ into an integer."""
  enc_iter = iter(enc)
  d = VLQ_DECODE_TABLE[next(enc_iter)]
  sign = bool(d & VLQ_SIGN_MASK)
  value = (d & VLQ_VALUE_MASK) >> 1
  # Compensate for first quantum containing sign as LSB:
  shift = -1

  while d & VLQ_MORE_MASK:
    shift += VLQ_VALUE_BITWIDTH
    d = VLQ_DECODE_TABLE[next(enc_iter)]
    value |= (d & VLQ_VALUE_MASK) << shift

  return -value if sign else value

