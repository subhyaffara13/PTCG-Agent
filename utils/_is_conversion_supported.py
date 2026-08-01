
def _is_conversion_supported(activation_post_process: torch.nn.Module) -> bool:
    dtype = activation_post_process.dtype  # type: ignore[attr-defined]

    is_dynamic = False
    if hasattr(activation_post_process, "is_dynamic"):
        is_dynamic = activation_post_process.is_dynamic  # type: ignore[attr-defined, assignment]

    return (
        (dtype in SUPPORTED_QDTYPES and (not is_dynamic))
        or is_dynamic  # type: ignore[return-value]
        or dtype == torch.float16
    )

