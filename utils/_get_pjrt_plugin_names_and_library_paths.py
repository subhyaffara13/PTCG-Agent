
def _get_pjrt_plugin_names_and_library_paths(
    plugins_from_env: str,
) -> dict[str, str]:
  """Gets the names and library paths of PJRT plugins to load from env var.

  Args:
    plugins_from_env: plugin name and paths from env var. It is in the format
      of 'name1:path1,name2:path2' ('name1;path1,name2;path2' for windows).

  Returns:
    A dict of {plugin_name: library path} for the PJRT plugins to load.
  """
  if not plugins_from_env:
    return {}

  pjrt_plugins = {}
  for plugin in plugins_from_env.split(','):
    try:
      name, library_path = plugin.split(os.path.pathsep)
      pjrt_plugins[name] = library_path
    except ValueError:
      logger.warning(
          'invalid value %s in env var PJRT_NAMES_AND_LIBRARY_PATHS %s',
          plugin,
          plugins_from_env,
      )
  return pjrt_plugins

