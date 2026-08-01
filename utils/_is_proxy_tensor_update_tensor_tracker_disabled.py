
def _is_proxy_tensor_update_tensor_tracker_disabled() -> bool:
    """
    Returns current state of disabling update tensor tracker.
    """
    return _disable_update_tensor_tracker_tls.value

