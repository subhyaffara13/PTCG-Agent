
def register_multi_flags_validator(flag_names,
                                   multi_flags_checker,
                                   message='Flags validation failed',
                                   flag_values=_flagvalues.FLAGS):
  """Adds a constraint to multiple flags.

  The constraint is validated when flags are initially parsed, and after each
  change of the corresponding flag's value.

  Args:
    flag_names: [str | FlagHolder], a list of the flag names or holders to be
        checked. Positional-only parameter.
    multi_flags_checker: callable, a function to validate the flag.

        * input - dict, with keys() being flag_names, and value for each key
            being the value of the corresponding flag (string, boolean, etc).
        * output - bool, True if validator constraint is satisfied.
            If constraint is not satisfied, it should either return False or
            raise flags.ValidationError.

    message: str, error text to be shown to the user if checker returns False.
        If checker raises flags.ValidationError, message from the raised
        error will be shown.
    flag_values: flags.FlagValues, optional FlagValues instance to validate
        against.

  Raises:
    AttributeError: Raised when a flag is not registered as a valid flag name.
    ValueError: Raised when multiple FlagValues are used in the same
        invocation. This can occur when FlagHolders have different `_flagvalues`
        or when str-type flag_names entries are present and the `flag_values`
        argument does not match that of provided FlagHolder(s).
  """
  flag_names, flag_values = _flagvalues.resolve_flag_refs(
      flag_names, flag_values)
  v = _validators_classes.MultiFlagsValidator(
      flag_names, multi_flags_checker, message)
  _add_validator(flag_values, v)

