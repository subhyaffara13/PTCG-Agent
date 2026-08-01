
def _init_backend(platform: str) -> xla_client.Client:
  registration = _backend_factories.get(platform, None)
  if registration is None:
    raise RuntimeError(
        f"Backend '{platform}' is not in the list of known backends: "
        f"{list(_backend_factories.keys())}.")

  if registration.experimental:
    logger.warning(f"Platform '{platform}' is experimental and not all JAX "
                   "functionality may be correctly supported!")
  logger.debug("Initializing backend '%s'", platform)
  backend = registration.factory()
  # TODO(skye): consider raising more descriptive errors directly from backend
  # factories instead of returning None.
  if backend is None:
    raise RuntimeError(f"Could not initialize backend '{platform}'")
  # TODO(b/356678989): Only check `backend.device_count()` when it counts
  # CPU-only devices.
  if backend.device_count() == 0 and len(backend._get_all_devices()) == 0:
    raise RuntimeError(f"Backend '{platform}' provides no devices.")
  util.distributed_debug_log(("Initialized backend", backend.platform),
                             ("process_index", backend.process_index()),
                             ("device_count", backend.device_count()),
                             ("local_devices", backend.local_devices()))
  logger.debug("Backend '%s' initialized", platform)
  for hook in _backend_initialization_hooks:
    hook(backend)
  return backend

