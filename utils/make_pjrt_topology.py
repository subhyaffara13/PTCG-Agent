
def make_pjrt_topology(platform: str, topology_name='', **kwargs):
  _discover_and_register_pjrt_plugins()
  actual_platform = canonicalize_platform(platform)
  with _backend_lock:
    if actual_platform in _topology_factories:
      return _topology_factories[actual_platform](topology_name, **kwargs)
  raise NotImplementedError("topology not implemented for %s" % platform)

