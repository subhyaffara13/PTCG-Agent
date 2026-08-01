
def current_flash_attention_impl() -> str | None:
    """
    Return the currently activated flash attention impl name, if any.

    ``None`` indicates that no custom impl has been activated.
    """
    return (
        _FLASH_ATTENTION_ACTIVE[0]
        if _FLASH_ATTENTION_ACTIVE is not None
        else _FLASH_ATTENTION_ACTIVE
    )

