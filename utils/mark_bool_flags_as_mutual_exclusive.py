
def mark_bool_flags_as_mutual_exclusive(flag_names, required=False,
                                        flag_values=_flagvalues.FLAGS):
  """Ensures that only one flag among flag_names is True.

  Args:
    flag_names: [str | FlagHolder], names or holders of flags.
        Positional-only parameter.
    required: bool. If true, exactly one flag must be True. Otherwise, at most
        one flag can be True, and it is valid for all flags to be False.
    flag_values: flags.FlagValues, optional FlagValues instance where the flags
        are defined.

  Raises:
    ValueError: Raised when multiple FlagValues are used in the same
        invocation. This can occur when FlagHolders have different `_flagvalues`
        or when str-type flag_names entries are present and the `flag_values`
        argument does not match that of provided FlagHolder(s).
  """
  flag_names, flag_values = _flagvalues.resolve_flag_refs(
      flag_names, flag_values)
  for flag_name in flag_names:
    if not flag_values[flag_name].boolean:
      raise _exceptions.ValidationError(
          'Flag --{} is not Boolean, which is required for flags used in '
          'mark_bool_flags_as_mutual_exclusive.'.format(flag_name))

  def validate_boolean_mutual_exclusion(flags_dict):
    flag_count = sum(bool(val) for val in flags_dict.values())
    if flag_count == 1 or (not required and flag_count == 0):
      return True
    raise _exceptions.ValidationError(
        '{} one of ({}) must be True.'.format(
            'Exactly' if required else 'At most', ', '.join(flag_names)))

  register_multi_flags_validator(
      flag_names, validate_boolean_mutual_exclusion, flag_values=flag_values)

