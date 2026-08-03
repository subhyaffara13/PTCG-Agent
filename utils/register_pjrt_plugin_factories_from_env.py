import os

def register_pjrt_plugin_factories_from_env() -> None:
  """Registers backend factories for PJRT plugins.

  A backend factory will be registered for every PJRT plugin in the input
  string, in the format of 'name1:path1,name2:path2' ('name1;path1,name2;path2'
  for windows). The path can be a path to the plugin library or a path to the
  plugin configuration json file. The json file needs to have a "library_path"
  field for the plugin library path. It can have an optional "create_option"
  field for the options used when creating a PJRT plugin client. The value of
  "create_option" is key-value pairs. Please see xla_client._NameValueMapping
  for the supported types of values.

  TPU PJRT plugin will be loaded and registered separately in make_tpu_client.
  """
  pjrt_plugins = _get_pjrt_plugin_names_and_library_paths(
      os.getenv('PJRT_NAMES_AND_LIBRARY_PATHS', '')
  )
  for plugin_name, path in pjrt_plugins.items():
    if path.endswith('.json'):
      library_path, options = _get_pjrt_plugin_config(path)
    else:
      library_path = path
      options = None
    logger.debug(
        'registering PJRT plugin %s from %s', plugin_name, library_path
    )
    register_plugin(plugin_name, library_path=library_path, options=options)

