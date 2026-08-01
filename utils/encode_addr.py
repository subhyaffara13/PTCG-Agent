
def encode_addr(x: int):
  result = (x & 0x3FFFF) >> 4
  if result << 4 != x:
    raise ValueError(f"Cannot encode value in an MMA descriptor: {x}")
  return result

