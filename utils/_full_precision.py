
def _full_precision(precision: Precision) -> tuple[Precision, Precision]:
  if precision is None or isinstance(precision, (DotAlgorithm, DotAlgorithmPreset)):
    return (Precision.DEFAULT, Precision.DEFAULT)
  elif not isinstance(precision, tuple):
    return (precision, precision)
  else:
    return precision

