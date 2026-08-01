
def _restore_device_fake_mode(tensor):
    if torch._guards.detect_fake_mode(None) is not None:
        if tensor.untyped_storage()._fake_device is not None:
            device = _get_restore_location(tensor.untyped_storage()._fake_device)
            if not isinstance(device, torch.device):
                device = torch.device(device)
            tensor.fake_device = torch.device(device)
    return tensor

