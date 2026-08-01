
def float32_to_uint32(n):
  packed = struct.pack("<1f", n)
  (converted,) = struct.unpack("<1L", packed)
  return converted

