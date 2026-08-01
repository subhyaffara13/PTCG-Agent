
def set_default(flag_holder: _flagvalues.FlagHolder[_T], value: _T) -> None:
  """Changes the default value of the provided flag object.

  The flag's current value is also updated if the flag is currently using
  the default value, i.e. not specified in the command line, and not set
  by FLAGS.name = value.

  Args:
    flag_holder: FlagHolder, the flag to modify.
    value: The new default value.

  Raises:
    IllegalFlagValueError: Raised when value is not valid.
  """
  flag_holder._flagvalues.set_default(flag_holder.name, value)  # pylint: disable=protected-access

