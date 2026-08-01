
def _DecodeFixed64(buffer, pos):
  """Decode a fixed64."""
  new_pos = pos + 8
  return (struct.unpack('<Q', buffer[pos:new_pos])[0], new_pos)

