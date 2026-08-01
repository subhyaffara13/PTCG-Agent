
def _clear_backends() -> None:
  global _backends
  global _backend_errors
  global _default_backend

  logger.debug("Clearing JAX backend caches.")
  with _backend_lock:
    _backends = {}
    _backend_errors = {}
    _default_backend = None

