
def _setup_canonical_aliases_for_api():
  import types  # pylint: disable=import-outside-toplevel

  for key, value in globals().items():
    if isinstance(value, (type, types.FunctionType)):
      canonical_aliases.add_alias(
          value, canonical_aliases.ModuleAttributePath(__name__, (key,))
      )

