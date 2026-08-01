
def make_c_api_device_topology(
    c_api: Any, topology_name: str = '', **kwargs
) -> DeviceTopology:
  """Creates a PJRT C API TopologyDescription."""
  return _xla.get_c_api_topology(c_api, topology_name, dict(**kwargs))

