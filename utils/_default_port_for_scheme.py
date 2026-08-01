
def _default_port_for_scheme(scheme: str) -> int:
    return 443 if scheme == "https" else 80

