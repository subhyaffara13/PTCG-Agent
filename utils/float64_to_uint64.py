
def float64_to_uint64(n):
  packed = struct.pack("<1d", n)
  (converted,) = struct.unpack("<1Q", packed)
  return converted

