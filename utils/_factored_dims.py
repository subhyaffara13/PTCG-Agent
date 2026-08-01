
def _factored_dims(
    shape: base.Shape, factored: bool, min_dim_size_to_factor: int
) -> Optional[tuple[int, int]]:
  """Whether to use a factored second moment estimator.

  This function returns a tuple with the two largest axes to reduce over.
  If no two dimensions have size >= min_dim_size_to_factor, return None.

  Args:
    shape: an input shape
    factored: whether to use factored second-moment estimator for 2d vars.
    min_dim_size_to_factor: only factor accumulator if two array dimensions have
      at least this size.

  Returns:
    None or a tuple of ints
  """
  if not factored or len(shape) < 2:
    return None
  sorted_dims = np.argsort(shape)
  if shape[sorted_dims[-2]] < min_dim_size_to_factor:
    return None
  return int(sorted_dims[-2]), int(sorted_dims[-1])

