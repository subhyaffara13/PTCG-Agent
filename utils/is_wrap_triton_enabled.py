
def is_wrap_triton_enabled() -> bool:
    return getattr(wrap_triton_enabled, "value", wrap_triton_enabled_default)

