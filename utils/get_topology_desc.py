
def get_topology_desc(
    topology_name: str = "", platform: str | None = None, **kwargs
) -> TopologyDescription:
  if platform == "tpu" or platform is None:
    return TopologyDescription(
        xb.make_pjrt_tpu_topology(
            topology_name, **kwargs
        )._make_compile_only_devices()
    )
  try:
    topology = xb.make_pjrt_topology(platform, topology_name, **kwargs)
    return TopologyDescription(topology._make_compile_only_devices())
  except _jax.JaxRuntimeError as e:
    msg, *_ = e.args
    if msg.startswith("UNIMPLEMENTED"):
      raise NotImplementedError(msg) from e
    else:
      raise

