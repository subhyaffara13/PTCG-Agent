
def initialize_pjrt_plugin(plugin_name: str) -> None:
  """Initializes a PJRT plugin.

  The plugin needs to be loaded first (through load_pjrt_plugin_dynamically or
  static linking) before this method is called.
  Args:
    plugin_name: the name of the PJRT plugin.
  """
  _xla.initialize_pjrt_plugin(plugin_name)

