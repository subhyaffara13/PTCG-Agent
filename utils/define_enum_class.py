
def DEFINE_enum_class(  # pylint: disable=invalid-name
    name: str,
    default: None | _ET | str,
    enum_class: type[_ET],
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    case_sensitive: bool = ...,
    *,
    required: Literal[True],
    **args: Any
) -> _flagvalues.FlagHolder[_ET]:
  ...


def DEFINE_enum_class(  # pylint: disable=invalid-name
    name: str,
    default: None,
    enum_class: type[_ET],
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    case_sensitive: bool = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[_ET | None]:
  ...


def DEFINE_enum_class(  # pylint: disable=invalid-name
    name: str,
    default: _ET | str,
    enum_class: type[_ET],
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    case_sensitive: bool = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[_ET]:
  ...


def DEFINE_enum_class(  # pylint: disable=invalid-name
    name,
    default,
    enum_class,
    help,  # pylint: disable=redefined-builtin
    flag_values=_flagvalues.FLAGS,
    module_name=None,
    case_sensitive=False,
    required=False,
    **args
):
  """Registers a flag whose value can be the name of enum members.

  Args:
    name: str, the flag name.
    default: Enum|str|None, the default value of the flag.
    enum_class: class, the Enum class with all the possible values for the flag.
    help: str, the help message.
    flag_values: :class:`FlagValues`, the FlagValues instance with which the
      flag will be registered. This should almost never need to be overridden.
    module_name: str, the name of the Python module declaring this flag. If not
      provided, it will be computed using the stack trace of this call.
    case_sensitive: bool, whether to map strings to members of the enum_class
      without considering case.
    required: bool, is this a required flag. This must be used as a keyword
      argument.
    **args: dict, the extra keyword args that are passed to ``Flag.__init__``.

  Returns:
    a handle to defined flag.
  """
  # NOTE: pytype fails if this is a direct return.
  result = DEFINE_flag(
      _flag.EnumClassFlag(
          name, default, help, enum_class, case_sensitive=case_sensitive, **args
      ),
      flag_values,
      module_name,
      required=True if required else False,
  )
  return result

