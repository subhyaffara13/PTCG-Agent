
def _sanitize_kernel_options_for_triton(
    kernel_options: dict[str, Any],
) -> tuple[dict[str, Any], _Backend]:
    """We always strip quotes around str values, we only need this in lowering, so we pop it here
    to avoid passing to triton constexpr dict
    """
    sanitized = dict(kernel_options)
    backend = cast(_Backend, sanitized.pop("BACKEND", "AUTO"))
    return sanitized, backend

