
def maybe_import_plugin_submodule(
    plugin_module_names: Sequence[str],
    submodule_name: str,
    *,
    check_version: bool = True,
) -> ModuleType | None:
  for plugin_module_name in plugin_module_names:
    try:
      module = importlib.import_module(
          f"{plugin_module_name}.{submodule_name}",
          package="jaxlib",
      )
    except ImportError:
      continue
    else:
      if not check_version:
        return module
      try:
        version_module = importlib.import_module(
            f"{plugin_module_name}.version",
            package="jaxlib",
        )
      except ImportError:
        return module
      plugin_version = getattr(version_module, "__version__", "")
      if check_plugin_version(
          plugin_module_name, jaxlib_version, plugin_version
      ):
        return module
  return None

