
def register_backend_initialization_hook(
    hook: Callable[[xla_client.Client], None],
) -> None:
  """Registers a callback to run on all initialized and future backends."""
  _backend_initialization_hooks.append(hook)
  with _backend_lock:
    for backend in _backends.values():
      hook(backend)

