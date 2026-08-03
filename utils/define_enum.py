from typing import Any

def DEFINE_enum(  # pylint: disable=invalid-name
    name: str,
    default: str | None,
    enum_values: Iterable[str],
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    *,
    required: Literal[True],
    **args: Any
) -> _flagvalues.FlagHolder[str]:
  ...


def DEFINE_enum(  # pylint: disable=invalid-name
    name: str,
    default: None,
    enum_values: Iterable[str],
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[str | None]:
  ...


def DEFINE_enum(  # pylint: disable=invalid-name
    name: str,
    default: str,
    enum_values: Iterable[str],
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[str]:
  ...


def DEFINE_enum(  # pylint: disable=invalid-name
    name,
    default,
    enum_values,
    help,  # pylint: disable=redefined-builtin
    flag_values=_flagvalues.FLAGS,
    module_name=None,
    required=False,
    **args
):
  """Registers a flag whose value can be any string from enum_values.

  Instead of a string enum, prefer `DEFINE_enum_class`, which allows
  defining enums from an `enum.Enum` class.

  Args:
    name: str, the flag name.
    default: str|None, the default value of the flag.
    enum_values: [str], a non-empty list of strings with the possible values for
      the flag.
    help: str, the help message.
    flag_values: :class:`FlagValues`, the FlagValues instance with which the
      flag will be registered. This should almost never need to be overridden.
    module_name: str, the name of the Python module declaring this flag. If not
      provided, it will be computed using the stack trace of this call.
    required: bool, is this a required flag. This must be used as a keyword
      argument.
    **args: dict, the extra keyword args that are passed to ``Flag.__init__``.

  Returns:
    a handle to defined flag.
  """
  result = DEFINE_flag(
      _flag.EnumFlag(name, default, help, enum_values, **args),
      flag_values,
      module_name,
      required=True if required else False,
  )
  return result

