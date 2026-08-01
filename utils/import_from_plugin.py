
def import_from_plugin(
    plugin_name: str, submodule_name: str, *, check_version: bool = True
) -> ModuleType | None:
  """Import a submodule from a known plugin with version checking.

  Args:
    plugin_name: The name of the plugin. The supported values are "cuda" or
      "rocm".
    submodule_name: The name of the submodule to import, e.g. "_triton".
    check_version: Whether to check that the plugin version is compatible with
      the jaxlib version. If the plugin is installed but the versions are not
      compatible, this function produces a warning and returns None.

  Returns:
    The imported submodule, or None if the plugin is not installed or if the
    versions are incompatible.
  """
  if plugin_name not in _PLUGIN_MODULE_NAMES:
    raise ValueError(f"Unknown plugin: {plugin_name}")
  return maybe_import_plugin_submodule(
      [f".{plugin_name}"] + _PLUGIN_MODULE_NAMES[plugin_name],
      submodule_name,
      check_version=check_version,
  )

