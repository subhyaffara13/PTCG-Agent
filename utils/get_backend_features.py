
def get_backend_features(
    device: torch.device | str | None,
) -> OrderedSet[BackendFeature]:
    if device is None:
        return OrderedSet()
    init_backend_registration()
    if isinstance(device, torch.device):
        device_type = device.type
    else:
        assert isinstance(device, str), type(device)
        device_type = device
        device = torch.device(device_type)
    scheduling_ctor = get_scheduling_for_device(device_type)
    assert scheduling_ctor
    scheduling = scheduling_ctor(None)
    return scheduling.get_backend_features(device)

