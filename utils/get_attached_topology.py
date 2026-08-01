
def get_attached_topology(platform=None) -> TopologyDescription:
  return TopologyDescription(jax.devices(backend=platform))

