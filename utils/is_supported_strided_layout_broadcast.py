
def is_supported_strided_layout_broadcast(
    src: WGStridedFragLayout,
    dst: WGStridedFragLayout,
    dims: tuple[int, ...],
) -> bool:
  """We only support broadcasting of leading dimensions."""
  if src.vec_size != dst.vec_size:
    return False
  # Check if input maps exactly to the end (prevents trailing dims).
  if dims != tuple(range(len(dst.shape) - len(src.shape), len(dst.shape))):
    return False
  # Identify input indices that are expanded vs. those that are preserved
  # Expansion: input is 1, output is > 1.
  # Preserved: input is > 1.
  exp_indices, pre_indices = [], []
  for i, dim in enumerate(src.shape):
    if dim == 1 and dst.shape[dims[i]] > 1:
      exp_indices.append(i)
    if dim > 1:
      pre_indices.append(i)
  # If both exist, all expansions must happen before all preserved
  # dimensions.
  if exp_indices and pre_indices and max(exp_indices) >= min(pre_indices):
    return False
  return True

