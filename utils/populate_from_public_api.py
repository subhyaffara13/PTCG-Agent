
def populate_from_public_api(
    module: types.ModuleType,
    predicate: Callable[
        [Any, ModuleAttributePath], bool
    ] = default_well_known_filter,
):
  """Populates canonical aliases with all public symbols in a module.

  Attempts to walk this module and its submodules to extract well-known symbols.
  Symbols that already have an alias defined will be ignored.

  If the module defines __all__, we assume the symbols in __all__ are the
  well-known symbols in this module. (See
  https://docs.python.org/3/reference/simple_stmts.html#the-import-statement)

  If the module does not define __all__, we look for all names that do not
  start with "_".

  We then additionally filter down this set to the set of objects for which
  the `predicate` argument returns True.

  This function should only be called on modules with a well-defined public API,
  that exports only functions defined in the module itself. If a module
  re-exports symbols from another external module (e.g. importing `partial`
  from `functools`), we might otherwise end up using the unrelated module as
  the "canonical" source of that object. (The `prefix_filter` function below
  tries to prevent this if possible when used as a predicate.)

  Args:
    module: The module we will collect symbols from.
    predicate: A filter function to check if an object should be given an alias.
  """
  if hasattr(module, "__all__"):
    public_names = module.__all__
  else:
    public_names = [
        key for key in module.__dict__.keys() if not key.startswith("_")
    ]

  for name in public_names:
    try:
      value = getattr(module, name)
    except AttributeError:
      # Possibly a misspecified __all__?
      continue
    path = ModuleAttributePath(module.__name__, (name,))
    if isinstance(value, types.ModuleType):
      if (
          value.__name__.startswith(module.__name__)
          and value.__name__ != module.__name__
      ):
        # Process submodules of this module also.
        populate_from_public_api(value, predicate)
      # Don't process external modules that are being re-exported.
    elif predicate(value, path):
      add_alias(value, path, on_conflict="ignore")

