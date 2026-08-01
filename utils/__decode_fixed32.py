
def _DecodeFixed32(buffer, pos):
  """Decode a fixed32."""

  new_pos = pos + 4
  return (struct.unpack('<I', buffer[pos:new_pos])[0], new_pos)

