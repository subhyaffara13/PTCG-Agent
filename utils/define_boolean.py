
def DEFINE_boolean(  # pylint: disable=invalid-name
    name: str,
    default: None | str | bool | int,
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    *,
    required: Literal[True],
    **args: Any
) -> _flagvalues.FlagHolder[bool]:
  ...


def DEFINE_boolean(  # pylint: disable=invalid-name
    name: str,
    default: None,
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[bool | None]:
  ...


def DEFINE_boolean(  # pylint: disable=invalid-name
    name: str,
    default: str | bool | int,
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[bool]:
  ...


def DEFINE_boolean(  # pylint: disable=invalid-name
    name,
    default,
    help,  # pylint: disable=redefined-builtin
    flag_values=_flagvalues.FLAGS,
    module_name=None,
    required=False,
    **args
):
  """Registers a boolean flag.

  Such a boolean flag does not take an argument.  If a user wants to
  specify a false value explicitly, the long option beginning with 'no'
  must be used: i.e. --noflag

  This flag will have a value of None, True or False.  None is possible
  if default=None and the user does not specify the flag on the command
  line.

  Args:
    name: str, the flag name.
    default: bool|str|None, the default value of the flag.
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
  return DEFINE_flag(  # pytype: disable=bad-return-type
      _flag.BooleanFlag(name, default, help, **args),
      flag_values,
      module_name,
      required=True if required else False,
  )

