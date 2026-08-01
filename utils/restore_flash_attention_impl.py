
def restore_flash_attention_impl(_raise_warn: bool = True) -> None:
    """
    Restore the default FA2 implementation
    """
    global _FLASH_ATTENTION_ACTIVE

    handle = None
    if _FLASH_ATTENTION_ACTIVE is not None:
        handle = _FLASH_ATTENTION_ACTIVE[1]

    if handle is not None:
        handle.remove()
    elif _raise_warn:
        logger.warning(
            "Trying to restore default FA2 impl when no custom impl was activated"
        )

    _FLASH_ATTENTION_ACTIVE = None  # default

