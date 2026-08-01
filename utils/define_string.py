
def DEFINE_string(  # pylint: disable=invalid-name
    name: str,
    default: str | None,
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    *,
    required: Literal[True],
    **args: Any
) -> _flagvalues.FlagHolder[str]:
  ...


def DEFINE_string(  # pylint: disable=invalid-name
    name: str,
    default: None,
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[str | None]:
  ...


def DEFINE_string(  # pylint: disable=invalid-name
    name: str,
    default: str,
    help: str | None,  # pylint: disable=redefined-builtin
    flag_values: _flagvalues.FlagValues = ...,
    required: bool = ...,
    **args: Any
) -> _flagvalues.FlagHolder[str]:
  ...


def DEFINE_string(  # pylint: disable=invalid-name
    name,
    default,
    help,  # pylint: disable=redefined-builtin
    flag_values=_flagvalues.FLAGS,
    required=False,
    **args
):
  """Registers a flag whose value can be any string."""
  parser = _argument_parser.ArgumentParser[str]()
  serializer = _argument_parser.ArgumentSerializer[str]()
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

