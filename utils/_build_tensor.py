
def _build_tensor(size, value=None, dtype=torch.float, device_id=None):
    if value is None:
        value = size
    if device_id is None:
        return torch.empty(size, size, size, dtype=dtype).fill_(value)
    else:
        return torch.empty(size, size, size, dtype=dtype).fill_(value).cuda(device_id)

