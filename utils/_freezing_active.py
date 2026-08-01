
def _freezing_active() -> bool:
    return getattr(_TLS, "freezing_active", False)

