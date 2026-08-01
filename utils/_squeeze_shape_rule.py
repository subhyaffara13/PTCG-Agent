
def _squeeze_shape_rule(operand, *, dimensions):
  return _compute_squeeze_shape(np.shape(operand), dimensions)

