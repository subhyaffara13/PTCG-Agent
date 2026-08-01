
def DEFINE_multi_enum(  # pylint: disable=invalid-name
    name: str,
    default: None | Iterable[str] | str,
    enum_values: Iterable[str],
    help: str,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    *,
    required: Literal[True],
    **args: Any
) -> _flagvalues.FlagHolder[list[str]]:
  ...


def DEFINE_multi_enum(  # pylint: disable=invalid-name
    name: str,
    default: None,
    enum_values: Iterable[str],
    help: str,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[list[str] | None]:
  ...


def DEFINE_multi_enum(  # pylint: disable=invalid-name
    name: str,
    default: Iterable[str] | str,
    enum_values: Iterable[str],
    help: str,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[list[str]]:
  ...


def DEFINE_multi_enum(  # pylint: disable=invalid-name
    name,
    default,
    enum_values,
    help,  # pylint: disable=redefined-builtin
    flag_values=_flagvalues.FLAGS,
    case_sensitive=True,
    required=False,
    **args
):
  """Registers a flag whose value can be a list strings from enum_values.

  Use the flag on the command line multiple times to place multiple
  enum values into the list.  The 'default' may be a single string
  (which will be converted into a single-element list) or a list of
  strings.

  Args:
    name: str, the flag name.
    default: Union[Iterable[str], str, None], the default value of the flag; see
      `DEFINE_multi`.
    enum_values: [str], a non-empty list of strings with the possible values for
      the flag.
    help: str, the help message.
    flag_values: :class:`FlagValues`, the FlagValues instance with which the
      flag will be registered. This should almost never need to be overridden.
    case_sensitive: Whether or not the enum is to be case-sensitive.
    required: bool, is this a required flag. This must be used as a keyword
      argument.
    **args: Dictionary with extra keyword args that are passed to the
      ``Flag.__init__``.

  Returns:
    a handle to defined flag.
  """
  parser = _argument_parser.EnumParser(enum_values, case_sensitive)
  serializer = _argument_parser.ArgumentSerializer()
  return DEFINE_multi(
      parser,
      serializer,
      name,
      default,
      '<%s>: %s' % ('|'.join(enum_values), help),
      flag_values,
      required=True if required else False,
      **args,
  )

