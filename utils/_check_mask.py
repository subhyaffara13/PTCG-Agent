
def _check_mask(mask: mask_lib.Mask) -> None:
  """Check that the given mask is valid.

  A row of all zeros along the kv dimension would result in a division by zero
  when computing the softmax. This function is meant to protect against that
  case.

  Args:
    mask: the mask to check.

  Raises:
    ValueError: the mask is invalid.
  """

  assert len(mask.shape) == 2

  exception_message = (
      'Some rows of the mask (along the kv dimension) are all zeros.\nThis is'
      ' would result in a division by zero when computing the attention'
      ' softmax.'
  )

  is_row_non_zero = np.zeros(mask.shape[0], dtype=np.bool_)
  for col in range(mask.shape[1]):
    # Mask only supports slice indices.
    is_row_non_zero = np.logical_or(
        is_row_non_zero,
        mask[(slice(0, mask.shape[0]), slice(col, col + 1))][:, 0],
    )
  if not is_row_non_zero.all():
    raise ValueError(exception_message)

