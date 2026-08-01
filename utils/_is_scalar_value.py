
def _is_scalar_value(value):
  if value.HasField('metadata') and value.metadata.HasField('plugin_data'):
    plugin_data = value.metadata.plugin_data
    return plugin_data.plugin_name == _SCALAR_PLUGIN_NAME

  return False

