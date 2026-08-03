from typing import Any

def DEFINE_alias(  # pylint: disable=invalid-name
    name: str,
    original_name: str,
    flag_values: _flagvalues.FlagValues = _flagvalues.FLAGS,
    module_name: str | None = None,
) -> _flagvalues.FlagHolder[Any]:
  """Defines an alias flag for an existing one.

  Args:
    name: str, the flag name.
    original_name: str, the original flag name.
    flag_values: :class:`FlagValues`, the FlagValues instance with which the
      flag will be registered. This should almost never need to be overridden.
    module_name: A string, the name of the module that defines this flag.

  Returns:
    a handle to defined flag.

  Raises:
    flags.FlagError:
      UnrecognizedFlagError: if the referenced flag doesn't exist.
      DuplicateFlagError: if the alias name has been used by some existing flag.
  """
  if original_name not in flag_values:
    raise _exceptions.UnrecognizedFlagError(original_name)
  flag = flag_values[original_name]

  class _FlagAlias(_flag.Flag):
    """Overrides Flag class so alias value is copy of original flag value."""

    def parse(self, argument):
      flag.parse(argument)
      self.present += 1

    def _parse_from_default(self, value):
      # The value was already parsed by the aliased flag, so there is no
      # need to call the parser on it a second time.
      # Additionally, because of how MultiFlag parses and merges values,
      # it isn't possible to delegate to the aliased flag and still get
      # the correct values.
      return value

    @property
    def value(self):
      return flag.value

    @value.setter
    def value(self, value):
      flag.value = value

  help_msg = 'Alias for --%s.' % flag.name
  # If alias_name has been used, flags.DuplicatedFlag will be raised.
  return DEFINE_flag(
      _FlagAlias(
          flag.parser,
          flag.serializer,
          name,
          flag.default,
          help_msg,
          boolean=flag.boolean), flag_values, module_name)

