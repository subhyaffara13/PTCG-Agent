
def backends_are_initialized() -> bool:
  "Returns true if backends have already been initialized."
  with _backend_lock:
    return len(_backends) != 0

