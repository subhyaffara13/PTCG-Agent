
def is_config_flag(flag):  # pylint: disable=g-bad-name
  """Returns True iff `flag` is an instance of `_ConfigFlag`.

  External users of the library may need to check if a flag is of this type
  or not, particularly because ConfigFlags should be parsed before any other
  flags. This function allows that test to be done without making the whole
  class public.

  Args:
    flag: Flag object.

  Returns:
    True iff `isinstance(flag, _ConfigFlag)` is true.
  """
  return isinstance(flag, _ConfigFlag)

