
def bitreflect(a, num_bits):
  """Reflects the bits of the given integer."""
  if a.bit_length() > num_bits:
    raise ValueError(f'Integer has more than {num_bits} bits')
  return sum(((a >> i) & 1) << (num_bits - 1 - i) for i in range(num_bits))

