import sys

def DEFINE_flag(  # pylint: disable=invalid-name
    flag: _flag.Flag[_T],
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    required: Literal[True] = ...,
) -> _flagvalues.FlagHolder[_T]:
  ...


def DEFINE_flag(  # pylint: disable=invalid-name
    flag: _flag.Flag[_T],
    flag_values: _flagvalues.FlagValues = ...,
    module_name: str | None = ...,
    required: bool = ...,
) -> _flagvalues.FlagHolder[_T | None]:
  ...


def DEFINE_flag(  # pylint: disable=invalid-name
    flag,
    flag_values=_flagvalues.FLAGS,
    module_name=None,
    required=False):
  """Registers a :class:`Flag` object with a :class:`FlagValues` object.

  By default, the global :const:`FLAGS` ``FlagValue`` object is used.

  Typical users will use one of the more specialized DEFINE_xxx
  functions, such as :func:`DEFINE_string` or :func:`DEFINE_integer`.  But
  developers who need to create :class:`Flag` objects themselves should use
  this function to register their flags.

  Args:
    flag: :class:`Flag`, a flag that is key to the module.
    flag_values: :class:`FlagValues`, the ``FlagValues`` instance with which the
      flag will be registered. This should almost never need to be overridden.
    module_name: str, the name of the Python module declaring this flag. If not
      provided, it will be computed using the stack trace of this call.
    required: bool, is this a required flag. This must be used as a keyword
      argument.

  Returns:
    a handle to defined flag.
  """
  if required and flag.default is not None:
    raise ValueError(
        'Required flag --%s needs to have None as default' % flag.name
    )
  # Copying the reference to flag_values prevents pychecker warnings.
  fv = flag_values
  fv[flag.name] = flag
  # Tell flag_values who's defining the flag.
  if module_name:
    module = sys.modules.get(module_name)
  else:
    module, module_name = _helpers.get_calling_module_object_and_name()
  flag_values.register_flag_by_module(module_name, flag)
  flag_values.register_flag_by_module_id(id(module), flag)
  if required:
    _validators.mark_flag_as_required(flag.name, fv)
  ensure_non_none_value = (flag.default is not None) or required
  return _flagvalues.FlagHolder(
      fv, flag, ensure_non_none_value=ensure_non_none_value)

