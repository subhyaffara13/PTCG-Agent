
def _shape_matches(actual_shape: Sequence[int],
                   expected_shape: _ai.TShapeMatcher) -> bool:
  """Returns True if `actual_shape` is compatible with `expected_shape`."""
  # Splits `expected_shape` based on the position of the ellipsis, if present.
  expected_prefix: List[_ai.TDimMatcher] = []
  expected_suffix: Optional[List[_ai.TDimMatcher]] = None
  for dim in expected_shape:
    if dim is Ellipsis:
      if expected_suffix is not None:
        raise ValueError(
            "`expected_shape` may not contain more than one ellipsis, "
            f"but got {_ai.format_shape_matcher(expected_shape)}")
      expected_suffix = []
    elif expected_suffix is None:
      expected_prefix.append(dim)
    else:
      expected_suffix.append(dim)

  # If there is no ellipsis, just compare to the full `actual_shape`.
  if expected_suffix is None:
    assert len(expected_prefix) == len(expected_shape)
    return _unelided_shape_matches(actual_shape, expected_prefix)

  # Checks that the actual rank is least the number of non-elided dimensions.
  if len(actual_shape) < len(expected_prefix) + len(expected_suffix):
    return False

  if expected_prefix:
    actual_prefix = actual_shape[:len(expected_prefix)]
    if not _unelided_shape_matches(actual_prefix, expected_prefix):
      return False

  if expected_suffix:
    actual_suffix = actual_shape[-len(expected_suffix):]
    if not _unelided_shape_matches(actual_suffix, expected_suffix):
      return False

  return True

