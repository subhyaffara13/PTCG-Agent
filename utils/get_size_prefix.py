
def GetSizePrefix(buf, offset):
  """Extract the size prefix from a buffer."""
  return encode.Get(packer.int32, buf, offset)

