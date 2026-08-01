
def _validate_operand_scale(
    side, operand, scale, contracting_dims: Sequence[int]
):
  for i, size in enumerate(operand.shape):
    if i in contracting_dims:
      if size % scale.shape[i] != 0:
        raise TypeError(
            f"{side} contracting dim {i} of size {size} must be divisible by "
            f"its scale's dim size {scale.shape[i]}."
        )
      s = size // scale.shape[i]
      if s < 2:
        raise TypeError(
            f"The ratio of {side} contracting dim {i} to its scale's dim size"
            f" ({s}) must be at least 2."
        )
    elif scale.shape[i] != size:
      raise TypeError(
          f"{side} dim {i} of size {size} does not match scale dim size "
          f"{scale.shape[i]}."
      )

