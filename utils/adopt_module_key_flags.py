
def adopt_module_key_flags(
    module: Any, flag_values: _flagvalues.FlagValues = _flagvalues.FLAGS
) -> None:
  """Declares that all flags key to a module are key to the current module.

  Args:
    module: module, the module object from which all key flags will be declared
      as key flags to the current module.
    flag_values: :class:`FlagValues`, the FlagValues instance in which the
      flags will be declared as key flags. This should almost never need to be
      overridden.

  Raises:
    Error: Raised when given an argument that is a module name (a string),
        instead of a module object.
  """
  if not isinstance(module, types.ModuleType):
    raise _exceptions.Error('Expected a module object, not %r.' % (module,))
  _internal_declare_key_flags(
      [f.name for f in flag_values.get_key_flags_for_module(module.__name__)],
      flag_values=flag_values)
  # If module is this flag module, take _helpers.SPECIAL_FLAGS into account.
  if module == _helpers.FLAGS_MODULE:
    _internal_declare_key_flags(
        # As we associate flags with get_calling_module_object_and_name(), the
        # special flags defined in this module are incorrectly registered with
        # a different module.  So, we can't use get_key_flags_for_module.
        # Instead, we take all flags from _helpers.SPECIAL_FLAGS (a private
        # FlagValues, where no other module should register flags).
        [_helpers.SPECIAL_FLAGS[name].name for name in _helpers.SPECIAL_FLAGS],
        flag_values=_helpers.SPECIAL_FLAGS,
        key_flag_values=flag_values)

