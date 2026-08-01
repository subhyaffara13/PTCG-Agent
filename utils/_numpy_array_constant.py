
def _numpy_array_constant(x: np.ndarray | np.generic) -> ir.Value:
  return hlo.constant(_numpy_array_attribute(x))

