
def _VarUInt64ByteSizeNoTag(uint64):
  """Returns the number of bytes required to serialize a single varint
  using boundary value comparisons. (unrolled loop optimization -WPierce)
  uint64 must be unsigned.
  """
  if uint64 <= 0x7f: return 1
  if uint64 <= 0x3fff: return 2
  if uint64 <= 0x1fffff: return 3
  if uint64 <= 0xfffffff: return 4
  if uint64 <= 0x7ffffffff: return 5
  if uint64 <= 0x3ffffffffff: return 6
  if uint64 <= 0x1ffffffffffff: return 7
  if uint64 <= 0xffffffffffffff: return 8
  if uint64 <= 0x7fffffffffffffff: return 9
  if uint64 > UINT64_MAX:
    raise message.EncodeError('Value out of range: %d' % uint64)
  return 10

