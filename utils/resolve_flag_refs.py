
def resolve_flag_refs(
    flag_refs: Sequence[str | FlagHolder], flag_values: FlagValues
) -> tuple[list[str], FlagValues]:
  """Helper to validate and resolve flag reference list arguments."""
  fv = None
  names = []
  for ref in flag_refs:
    if isinstance(ref, FlagHolder):
      newfv = ref._flagvalues  # pylint: disable=protected-access
      name = ref.name
    else:
      newfv = flag_values
      name = ref
    if fv and fv != newfv:
      raise ValueError(
          'multiple FlagValues instances used in invocation. '
          'FlagHolders must be registered to the same FlagValues instance as '
          'do flag names, if provided.'
      )
    fv = newfv
    names.append(name)
  if fv is None:
    raise ValueError('flag_refs argument must not be empty')
  return names, fv

