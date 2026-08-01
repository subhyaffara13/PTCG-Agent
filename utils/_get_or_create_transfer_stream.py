
def _get_or_create_transfer_stream(device: torch.device) -> torch.Stream:
    if device not in _transfer_streams:
        _transfer_streams[device] = torch.Stream(device=device)
    return _transfer_streams[device]

