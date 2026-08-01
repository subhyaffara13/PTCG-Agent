
def _in_hop_compile() -> bool:
    return getattr(_hop_compile_tls, "in_hop_compile", False)

