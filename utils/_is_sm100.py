
def _is_sm100(device: torch.device) -> bool:
    """``True`` for Blackwell (SM100+). Cached: device capability is fixed for the
    process lifetime and this gets hit on every linear/expert forward.
    """
    return torch.cuda.get_device_capability(device)[0] >= 10

