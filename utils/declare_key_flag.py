
def declare_key_flag(
    flag_name: str | _flagvalues.FlagHolder,
    flag_values: _flagvalues.FlagValues = _flagvalues.FLAGS,
) -> None:
  """Declares one flag as key to the current module.

  Key flags are flags that are deemed really important for a module.
  They are important when listing help messages; e.g., if the
  --helpshort command-line flag is used, then only the key flags of the
  main module are listed (instead of all flags, as in the case of
  --helpfull).

  Sample usage::

      flags.declare_key_flag('flag_1')

  Args:
    flag_name: str | :class:`FlagHolder`, the name or holder of an already
      declared flag. (Redeclaring flags as key, including flags implicitly key
      because they were declared in this module, is a no-op.)
      Positional-only parameter.
    flag_values: :class:`FlagValues`, the FlagValues instance in which the
      flag will be declared as a key flag. This should almost never need to be
      overridden.

  Raises:
    ValueError: Raised if flag_name not defined as a Python flag.
  """
  flag_name, flag_values = _flagvalues.resolve_flag_ref(flag_name, flag_values)
  if flag_name in _helpers.SPECIAL_FLAGS:
    # Take care of the special flags, e.g., --flagfile, --undefok.
    # These flags are defined in SPECIAL_FLAGS, and are treated
    # specially during flag parsing, taking precedence over the
    # user-defined flags.
    _internal_declare_key_flags([flag_name],
                                flag_values=_helpers.SPECIAL_FLAGS,
                                key_flag_values=flag_values)
    return
  try:
    _internal_declare_key_flags([flag_name], flag_values=flag_values)
  except KeyError:
    raise ValueError('Flag --%s is undefined. To set a flag as a key flag '
                     'first define it in Python.' % flag_name)

