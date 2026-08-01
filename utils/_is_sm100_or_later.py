
def _is_sm100_or_later():
    """Check if we're on SM100+ hardware (Blackwell)."""
    return torch.cuda.is_available() and torch.cuda.get_device_capability() >= (10, 0)

