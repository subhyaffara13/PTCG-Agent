
def _use_torchcomms_enabled() -> bool:
    """Check if torchcomms is enabled via config."""
    return _TORCHCOMM_AVAILABLE and dist_config.use_torchcomms

