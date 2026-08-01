
def is_floating_dtype(dtype: numpy.typing.DTypeLike) -> bool:
  """Returns whether the given dtype is a floating dtype.

  Supports both basic numpy dtypes and the extended dtypes in the `ml_dtypes`
  package (if installed).

  Args:
    dtype: The dtype to check.

  Returns:
    True if the given dtype is a floating dtype.
  """
  dtype = np.dtype(dtype)
  if np.issubdtype(dtype, np.floating):
    return True
  if isinstance(dtype.type, type) and dtype.type.__module__ == "ml_dtypes":
    import ml_dtypes  # pylint: disable=import-outside-toplevel

    try:
      _ = ml_dtypes.finfo(dtype)
      return True
    except ValueError:
      return False
  return False

