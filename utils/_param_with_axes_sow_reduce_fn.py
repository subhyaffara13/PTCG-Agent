
def _param_with_axes_sow_reduce_fn(x, y):
  """Reduction function for sow() calls.

  Args:
    x: Existing value, or () if there was none.
    y: New axis names sown.

  Returns:
    New axis names.

  Raises:
    TypeError: If the newly sown value is not an AxisMetadata.
    ValueError: If the newly sown axis names don't match previously sown axis
      names.
    AssertionError: If a previously sown value was truthy and not an
      AxisMetadata.
  """
  if not isinstance(y, AxisMetadata):
    raise TypeError('Expected newly sown value to be an AxisMetadata')

  if isinstance(x, AxisMetadata):
    if x != y:
      raise ValueError(
          'If axis names are sown twice, expected them to match. '
          f'Got {x} and {y}.'
      )
  elif x:
    # Shouldn't happen, so raise a fairly internal error.
    raise AssertionError(f'Non-initial-or-AxisMetadata value encountered: {x}')
  return y

