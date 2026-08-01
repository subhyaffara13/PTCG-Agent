
def _SignedVarintDecoder(bits, result_type):
  """Like _VarintDecoder() but decodes signed values."""

  signbit = 1 << (bits - 1)
  mask = (1 << bits) - 1

  def DecodeVarint(buffer, pos):
    result = 0
    shift = 0
    while 1:
      b = buffer[pos]
      result |= ((b & 0x7f) << shift)
      pos += 1
      if not (b & 0x80):
        result &= mask
        result = (result ^ signbit) - signbit
        result = result_type(result)
        return (result, pos)
      shift += 7
      if shift >= 64:
        raise _DecodeError('Too many bytes when decoding varint.')
  return DecodeVarint

