
def can_convert_to_tracable_parameter() -> bool:
    return getattr(_TLS, "convert_tracable_parameter", True)

