
def DEFINE_path(  # pylint: disable=invalid-name
    name: str,
    default: None,
    help: str,  # pylint: disable=redefined-builtin
    flag_values: flags.FlagValues = ...,
    *,
    required: Literal[True],
    **kwargs,
) -> flags.FlagHolder[abstract_path.Path]:
  ...


def DEFINE_path(  # For consistency with other flags, pylint: disable=invalid-name
    name: str,
    default: None,
    help: str,  # pylint: disable=redefined-builtin
    flag_values: flags.FlagValues = ...,
    *,
    required: Literal[False] = False,
    **kwargs,
) -> flags.FlagHolder[Optional[abstract_path.Path]]:
  ...


def DEFINE_path(  # For consistency with other flags, pylint: disable=invalid-name
    name: str,
    default: epath_typing.PathLike,
    help: str,  # pylint: disable=redefined-builtin
    flag_values: flags.FlagValues = ...,
    *,
    required: Literal[False] = False,
    **kwargs,
) -> flags.FlagHolder[abstract_path.Path]:
  ...


def DEFINE_path(  # pylint: disable=invalid-name
    name,
    default,
    help,  # pylint: disable=redefined-builtin
    flag_values=None,
    *,
    required=False,
    **kwargs,
):
  """Defines a flag containing a epath.Path value."""

  # Lazy-import as absl is an optional dep
  from absl import flags  # pylint: disable=g-import-not-at-top

  if flag_values is None:
    flag_values = flags.FLAGS

  class _PathParser(flags.ArgumentParser):

    def parse(self, value):
      return abstract_path.Path(value)

  class _PathSerializer(flags.ArgumentSerializer):

    def serialize(self, value):
      return os.fspath(value)

  return flags.DEFINE(
      _PathParser(),
      name,
      default,
      help,
      flag_values,
      _PathSerializer(),
      required=required,
      **kwargs,
  )  # pytype: disable=bad-return-type

