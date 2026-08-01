
def has_compilation_handler(platform: str) -> bool:
  platform = platform.upper()
  with _compilation_handlers_lock:
    return platform in _compilation_handlers

