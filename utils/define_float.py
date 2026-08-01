
def DEFINE_float(  # pylint: disable=invalid-name
    name: str,
    default: None | float | str,
    help: str | None,  # pylint: disable=redefined-builtin
    lower_bound: float | None = ...,
    upper_bound: float | None = ...,
    flag_values: _flagvalues.FlagValues = ...,
    *,
    required: Literal[True],
    **args: Any
) -> _flagvalues.FlagHolder[float]:
  ...


def DEFINE_float(  # pylint: disable=invalid-name
    name: str,
    default: None,
    help: str | None,  # pylint: disable=redefined-builtin
    lower_bound: float | None = ...,
    upper_bound: float | None = ...,
    flag_values: _flagvalues.FlagValues = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[float | None]:
  ...


def DEFINE_float(  # pylint: disable=invalid-name
    name: str,
    default: float | str,
    help: str | None,  # pylint: disable=redefined-builtin
    lower_bound: float | None = ...,
    upper_bound: float | None = ...,
    flag_values: _flagvalues.FlagValues = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[float]:
  ...


def DEFINE_float(  # pylint: disable=invalid-name
    name,
    default,
    help,  # pylint: disable=redefined-builtin
    lower_bound=None,
    upper_bound=None,
    flag_values=_flagvalues.FLAGS,
    required=False,
    **args
):
  """Registers a flag whose value must be a float.

  If ``lower_bound`` or ``upper_bound`` are set, then this flag must be
  within the given range.

  Args:
    name: str, the flag name.
    default: float|str|None, the default value of the flag.
    help: str, the help message.
    lower_bound: float, min value of the flag.
    upper_bound: float, max value of the flag.
    flag_values: :class:`FlagValues`, the FlagValues instance with which the
      flag will be registered. This should almost never need to be overridden.
    required: bool, is this a required flag. This must be used as a keyword
      argument.
    **args: dict, the extra keyword args that are passed to :func:`DEFINE`.

  Returns:
    a handle to defined flag.
  """
  parser = _argument_parser.FloatParser(lower_bound, upper_bound)
  serializer = _argument_parser.ArgumentSerializer()
  result = DEFINE(
      parser,
      name,
      default,
      help,  # pylint: disable=redefined-builtin
      flag_values,
      serializer,
      required=True if required else False,
      **args,
  )
  _register_bounds_validator_if_needed(parser, name, flag_values=flag_values)
  return result

