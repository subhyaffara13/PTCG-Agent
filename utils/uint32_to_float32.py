
def uint32_to_float32(n):
  packed = struct.pack("<1L", n)
  (unpacked,) = struct.unpack("<1f", packed)
  return unpacked


def uint32_to_float32(u):
    return ((u >> np.uint32(8)) * (1.0 / 2**24)).astype(np.float32)

