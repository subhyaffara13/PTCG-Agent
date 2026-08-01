
def _ensure_backends_initialized(platforms: tuple[str,...]):
  """Ensure FFI handlers are initialized for the given platforms"""
  if "cpu" in platforms:
    linalg.initialize_lapack()

