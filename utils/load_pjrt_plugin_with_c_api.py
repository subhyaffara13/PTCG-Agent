
def load_pjrt_plugin_with_c_api(plugin_name: str, c_api: Any) -> None:
  _xla.load_pjrt_plugin(plugin_name, None, c_api)

