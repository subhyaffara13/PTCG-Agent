
def _rng_algorithm(algorithm: RandomAlgorithm):
  if algorithm == RandomAlgorithm.RNG_THREE_FRY:
    return hlo.RngAlgorithmAttr.get("THREE_FRY")
  elif algorithm == RandomAlgorithm.RNG_PHILOX:
    return hlo.RngAlgorithmAttr.get("PHILOX")
  elif algorithm == RandomAlgorithm.RNG_DEFAULT:
    return hlo.RngAlgorithmAttr.get("DEFAULT")
  else:
    assert False

