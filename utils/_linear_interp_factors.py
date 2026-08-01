
def _linear_interp_factors(
    old_min: _MinMaxValue,
    old_max: _MinMaxValue,
    new_min: _MinMaxValue,
    new_max: _MinMaxValue,
) -> Tuple[Union[float, FloatArray['d']], Union[float, FloatArray['d']]]:
  """Resolve the `y = a * x + b` equation and returns the factors."""
  a = (new_min - new_max) / (old_min - old_max)
  b = (old_min * new_max - new_min * old_max) / (old_min - old_max)
  return a, b

