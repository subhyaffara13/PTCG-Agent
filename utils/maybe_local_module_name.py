
def maybe_local_module_name(module: types.ModuleType) -> str:
  """Returns a name for this module, possibly looking up local aliases."""
  alias = lookup_alias(module, allow_outdated=True, allow_relative=True)
  assert alias is not None
  return str(alias)

