from typing import Any

def register_backend_factory(name: str, factory: BackendFactory, *,
                             priority: int = 0,
                             fail_quietly: bool = True,
                             experimental: bool = False,
                             make_topology: TopologyFactory | None = None,
                             c_api: Any | None = None) -> None:
  with _backend_lock:
    if name in _backends:
      raise RuntimeError(f"Backend {name} already initialized")
  _backend_factories[name] = BackendRegistration(
    factory, priority, fail_quietly, experimental, c_api)
  if make_topology is not None:
    _topology_factories[name] = make_topology

