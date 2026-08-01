
def _split_shape_rule(operand, *, sizes, axis):
  shapes = []
  shape = list(operand.shape)
  if any(s < 0 for s in sizes):
    raise ValueError(
      f"Sizes passed to split must be nonnegative, got {list(sizes)}")
  if operand.shape[axis] != np.sum(sizes):
    raise ValueError(
      f"Sum of sizes {np.sum(sizes)} must be equal to dimension {axis} of the "
      f"operand shape {list(operand.shape)}")
  for size in sizes:
    shape[axis] = size
    shapes.append(tuple(shape))
  return shapes

