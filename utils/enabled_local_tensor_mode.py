
def enabled_local_tensor_mode() -> LocalTensorMode | None:
    """
    Returns the current active LocalTensorMode only if it's enabled.

    This is a convenience function that combines the common pattern of checking
    if local_tensor_mode() is not None and not disabled.

    Returns:
        Optional[LocalTensorMode]: The current LocalTensorMode if active and enabled, else None.
    """
    lm = local_tensor_mode()
    if lm is not None and not lm._disable:
        return lm
    return None

