
def _get_backend_stream(priority: int = 0) -> torch.cuda.Stream:
    if priority not in _backend_streams:
        _backend_streams[priority] = torch.cuda.Stream(priority=priority)
    return _backend_streams[priority]

