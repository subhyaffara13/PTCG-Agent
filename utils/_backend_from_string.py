
def _backend_from_string(name: str):
    return getattr(SDPBackend, name)

