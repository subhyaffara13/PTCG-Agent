import sys

def disclaim_key_flags() -> None:
  """Declares that the current module will not define any more key flags.

  Normally, the module that calls the DEFINE_xxx functions claims the
  flag to be its key flag.  This is undesirable for modules that
  define additional DEFINE_yyy functions with its own flag parsers and
  serializers, since that module will accidentally claim flags defined
  by DEFINE_yyy as its key flags.  After calling this function, the
  module disclaims flag definitions thereafter, so the key flags will
  be correctly attributed to the caller of DEFINE_yyy.

  After calling this function, the module will not be able to define
  any more flags.  This function will affect all FlagValues objects.
  """
  globals_for_caller = sys._getframe(1).f_globals  # pylint: disable=protected-access
  module = _helpers.get_module_object_and_name(globals_for_caller)
  if module is not None:
    _helpers.disclaim_module_ids.add(id(module.module))

