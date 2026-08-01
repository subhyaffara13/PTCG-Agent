
def load_pjrt_plugin_dynamically(plugin_name: str, library_path: str) -> Any:
  return _xla.load_pjrt_plugin(plugin_name, library_path, c_api=None)

