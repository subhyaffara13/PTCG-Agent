from typing import Any

def DEFINE_multi_enum_class(  # pylint: disable=invalid-name
    name: str,
    # This is separate from `Union[None, _ET, Iterable[str], str]` to avoid a
    # Pytype issue inferring the return value to
    # FlagHolder[List[Union[_ET, enum.Enum]]] when an iterable of concrete enum
    # subclasses are used.
    default: Iterable[_ET],
    enum_class: type[_ET],
    help: str,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    *,
    required: Literal[True],
    **args: Any
) -> _flagvalues.FlagHolder[list[_ET]]:
  ...


def DEFINE_multi_enum_class(  # pylint: disable=invalid-name
    name: str,
    default: None | _ET | Iterable[str] | str,
    enum_class: type[_ET],
    help: str,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    *,
    required: Literal[True],
    **args: Any
) -> _flagvalues.FlagHolder[list[_ET]]:
  ...


def DEFINE_multi_enum_class(  # pylint: disable=invalid-name
    name: str,
    default: None,
    enum_class: type[_ET],
    help: str,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[list[_ET] | None]:
  ...


def DEFINE_multi_enum_class(  # pylint: disable=invalid-name
    name: str,
    # This is separate from `Union[None, _ET, Iterable[str], str]` to avoid a
    # Pytype issue inferring the return value to
    # FlagHolder[List[Union[_ET, enum.Enum]]] when an iterable of concrete enum
    # subclasses are used.
    default: Iterable[_ET],
    enum_class: type[_ET],
    help: str,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[list[_ET]]:
  ...


def DEFINE_multi_enum_class(  # pylint: disable=invalid-name
    name: str,
    default: _ET | Iterable[str] | str,
    enum_class: type[_ET],
    help: str,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[list[_ET]]:
  ...


def DEFINE_multi_enum_class(  # pylint: disable=invalid-name
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
  """Registers a flag whose value can be a list of enum members.

  Use the flag on the command line multiple times to place multiple
  enum values into the list.

  Args:
    name: str, the flag name.
    default: Union[Iterable[Enum], Iterable[str], Enum, str, None], the default
      value of the flag; see `DEFINE_multi`; only differences are documented
      here. If the value is a single Enum, it is treated as a single-item list
      of that Enum value. If it is an iterable, text values within the iterable
      will be converted to the equivalent Enum objects.
    enum_class: class, the Enum class with all the possible values for the flag.
    help: str, the help message.
    flag_values: :class:`FlagValues`, the FlagValues instance with which the
      flag will be registered. This should almost never need to be overridden.
    module_name: A string, the name of the Python module declaring this flag. If
      not provided, it will be computed using the stack trace of this call.
    case_sensitive: bool, whether to map strings to members of the enum_class
      without considering case.
    required: bool, is this a required flag. This must be used as a keyword
      argument.
    **args: Dictionary with extra keyword args that are passed to the
      ``Flag.__init__``.

  Returns:
    a handle to defined flag.
  """
  # NOTE: pytype fails if this is a direct return.
  result = DEFINE_flag(
      _flag.MultiEnumClassFlag(
          name,
          default,
          help,
          enum_class,
          case_sensitive=case_sensitive,
          **args,
      ),
      flag_values,
      module_name,
      required=True if required else False,
  )
  return result

