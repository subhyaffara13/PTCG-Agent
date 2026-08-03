import json

def _get_pjrt_plugin_config(
    json_path: str,
) -> tuple[
    str, Mapping[str, str | int | list[int] | float | bool] | None
]:
  """Gets PJRT plugin configuration from a json file.

  The json file needs to have a "library_path" field for the plugin library
  path. It can have an optional "create_option" field for the options used when
  creating a PJRT plugin client. The value of "create_option" is key-value
  pairs. Please see xla_client._NameValueMapping for the supported types of
  values.
  """
  with open(json_path) as f:
    config = json.load(f)
  if 'library_path' not in config.keys():
    raise ValueError(
        'PJRT plugin config file should contain "library_path" field.'
    )
  return (config['library_path'], config.get('create_options'))

