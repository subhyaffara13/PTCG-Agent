
def GetRoot(buf):
  """Returns root `Ref` object for the given buffer."""
  if len(buf) < 3:
    raise ValueError('buffer is too small')
  byte_width = buf[-1]
  return Ref.PackedType(
      Buf(buf, -(2 + byte_width)), byte_width, packed_type=buf[-2]
  )

