
def resolve_flag_ref(
    flag_ref: str | FlagHolder, flag_values: FlagValues
) -> tuple[str, FlagValues]:
  """Helper to validate and resolve a flag reference argument."""
  if isinstance(flag_ref, FlagHolder):
    new_flag_values = flag_ref._flagvalues  # pylint: disable=protected-access
    if flag_values != FLAGS and flag_values != new_flag_values:
      raise ValueError(
          'flag_values must not be customized when operating on a FlagHolder'
      )
    return flag_ref.name, new_flag_values
  return flag_ref, flag_values

