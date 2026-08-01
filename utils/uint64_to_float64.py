
def uint64_to_float64(n):
  packed = struct.pack("<1Q", n)
  (unpacked,) = struct.unpack("<1d", packed)
  return unpacked

