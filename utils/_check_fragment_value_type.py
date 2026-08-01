
def _check_fragment_value_type(
    value: Any,
    valid_types: type[Any] | tuple[type[Any], ...],
) -> None:
  """Checks that the value has the correct type, with a nice error message."""
  if not isinstance(value, valid_types):
    if not isinstance(valid_types, tuple):
      valid_types = (valid_types,)
    raise TypeError(
        'Fragment value must be a'
        f' {" or ".join(_qualified_name(t) for t in valid_types)}, not'
        f' {type(value)}.'
    )

