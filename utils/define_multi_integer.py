from typing import Any

def DEFINE_multi_integer(  # pylint: disable=invalid-name
    name: str,
    default: None | Iterable[int] | int | str,
    help: str,  # pylint: disable=redefined-builtin
    lower_bound: int | None = ...,
    upper_bound: int | None = ...,
    flag_values: _flagvalues.FlagValues = ...,
    *,
    required: Literal[True],
    **args: Any
) -> _flagvalues.FlagHolder[list[int]]:
  ...


def DEFINE_multi_integer(  # pylint: disable=invalid-name
    name: str,
    default: None,
    help: str,  # pylint: disable=redefined-builtin
    lower_bound: int | None = ...,
    upper_bound: int | None = ...,
    flag_values: _flagvalues.FlagValues = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[list[int] | None]:
  ...


def DEFINE_multi_integer(  # pylint: disable=invalid-name
    name: str,
    default: Iterable[int] | int | str,
    help: str,  # pylint: disable=redefined-builtin
    lower_bound: int | None = ...,
    upper_bound: int | None = ...,
    flag_values: _flagvalues.FlagValues = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[list[int]]:
  ...


def DEFINE_multi_integer(  # pylint: disable=invalid-name
    name,
    default,
    help,  # pylint: disable=redefined-builtin
    lower_bound=None,
    upper_bound=None,
    flag_values=_flagvalues.FLAGS,
    required=False,
    **args
):
  """Registers a flag whose value can be a list of arbitrary integers.

  Use the flag on the command line multiple times to place multiple
  integer values into the list.  The 'default' may be a single integer
  (which will be converted into a single-element list) or a list of
  integers.

  Args:
    name: str, the flag name.
    default: Union[Iterable[int], str, None], the default value of the flag; see
      `DEFINE_multi`.
    help: str, the help message.
    lower_bound: int, min values of the flag.
    upper_bound: int, max values of the flag.
    flag_values: :class:`FlagValues`, the FlagValues instance with which the
      flag will be registered. This should almost never need to be overridden.
    required: bool, is this a required flag. This must be used as a keyword
      argument.
    **args: Dictionary with extra keyword args that are passed to the
      ``Flag.__init__``.

  Returns:
    a handle to defined flag.
  """
  parser = _argument_parser.IntegerParser(lower_bound, upper_bound)
  serializer = _argument_parser.ArgumentSerializer()
  return DEFINE_multi(
      parser,
      serializer,
      name,
      default,
      help,  # pylint: disable=redefined-builtin
      flag_values,
      required=True if required else False,
      **args,
  )

