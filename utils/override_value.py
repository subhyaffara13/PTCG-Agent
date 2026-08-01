
def override_value(flag_holder: _flagvalues.FlagHolder[_T], value: _T) -> None:
  """Overrides the value of the provided flag.

  This value takes precedent over the default value and, when called after flag
  parsing, any value provided at the command line.

  Args:
    flag_holder: FlagHolder, the flag to modify.
    value: The new value.

  Raises:
    IllegalFlagValueError: The value did not pass the flag parser or validators.
  """
  fv = flag_holder._flagvalues  # pylint: disable=protected-access
  # Ensure the new value satisfies the flag's parser while avoiding side
  # effects of calling parse().
  parsed = fv[flag_holder.name]._parse(value)  # pylint: disable=protected-access
  if parsed != value:
    raise _exceptions.IllegalFlagValueError(
        'flag %s: parsed value %r not equal to original %r'
        % (flag_holder.name, parsed, value)
    )
  setattr(fv, flag_holder.name, value)

