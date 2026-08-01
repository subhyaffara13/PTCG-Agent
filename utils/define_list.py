
def DEFINE_list(  # pylint: disable=invalid-name
    name: str,
    default: None | Iterable[str] | str,
    help: str,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    *,
    required: Literal[True],
    **args: Any
) -> _flagvalues.FlagHolder[list[str]]:
  ...


def DEFINE_list(  # pylint: disable=invalid-name
    name: str,
    default: None,
    help: str,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[list[str] | None]:
  ...


def DEFINE_list(  # pylint: disable=invalid-name
    name: str,
    default: Iterable[str] | str,
    help: str,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[list[str]]:
  ...


def DEFINE_list(  # pylint: disable=invalid-name
    name,
    default,
    help,  # pylint: disable=redefined-builtin
    flag_values=_flagvalues.FLAGS,
    required=False,
    **args
):
  """Registers a flag whose value is a comma-separated list of strings.

  The flag value is parsed with a CSV parser.

  Args:
    name: str, the flag name.
    default: list|str|None, the default value of the flag.
    help: str, the help message.
    flag_values: :class:`FlagValues`, the FlagValues instance with which the
      flag will be registered. This should almost never need to be overridden.
    required: bool, is this a required flag. This must be used as a keyword
      argument.
    **args: Dictionary with extra keyword args that are passed to the
      ``Flag.__init__``.

  Returns:
    a handle to defined flag.
  """
  parser = _argument_parser.ListParser()
  serializer = _argument_parser.CsvListSerializer(',')
  return DEFINE(
      parser,
      name,
      default,
      help,
      flag_values,
      serializer,
      required=True if required else False,
      **args,
  )

