
def stochastic_round(x, random_bits, *, target_dtype):
  return stochastic_round_p.bind(x, random_bits, target_dtype=target_dtype)

