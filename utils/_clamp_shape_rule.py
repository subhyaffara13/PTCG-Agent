
def _clamp_shape_rule(min, operand, max):
  if min.shape and min.shape != operand.shape:
    raise TypeError("clamp requires min.shape == operand.shape or min.shape == "
                    f"(), got min.shape={min.shape}, {operand.shape=}.")
  if max.shape and max.shape != operand.shape:
    raise TypeError("clamp requires max.shape == operand.shape or max.shape == "
                    f"(), got max.shape={max.shape}, {operand.shape=}.")
  return operand.shape

