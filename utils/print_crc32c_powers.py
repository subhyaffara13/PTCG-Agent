
def print_crc32c_powers():
  """Generates kCRC32CPowers[].

  kCRC32CPowers[] is an array of length NUM_SIZE_BITS - NUM_DROPPED_BITS,
  whose i'th entry is x^(2^(i + LOG2_BITS_PER_BYTE + NUM_DROPPED_BITS) -
  CRC_BITS - 1) mod G. See kCRC32CPowers[] in the C++ source for more info.
  """
  for i in range(NUM_SIZE_BITS - NUM_DROPPED_BITS):
    poly = poly_exp(
        X,
        2 ** (i + LOG2_BITS_PER_BYTE + NUM_DROPPED_BITS)
        - CRC_BITS
        - (1 if LSB_FIRST else 0),
        G,
    )
    poly = bitreflect(poly, CRC_BITS)
    print(f'0x{poly:0{2*CRC_BITS//8}x}, ', end='')

