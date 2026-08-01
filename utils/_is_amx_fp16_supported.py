
def _is_amx_fp16_supported() -> bool:
    r"""Returns a bool indicating if CPU supports AMX FP16."""
    return get_capabilities().get("amx_fp16", False)

