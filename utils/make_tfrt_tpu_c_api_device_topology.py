
def make_tfrt_tpu_c_api_device_topology(
    topology_name: str = '', **kwargs
) -> DeviceTopology:
  """Creates a PJRT C API TopologyDescription."""
  return _xla.get_default_c_api_topology('tpu', topology_name, dict(**kwargs))

