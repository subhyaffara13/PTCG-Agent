
def _is_amx_tile_supported() -> bool:
    r"""Returns a bool indicating if CPU supports AMX_TILE."""
    return get_capabilities().get("amx_tile", False)

