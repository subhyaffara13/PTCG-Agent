
def list_flash_attention_impls() -> list[str]:
    """Return the names of all available flash attention implementations."""
    return sorted(_FLASH_ATTENTION_IMPLS.keys())

