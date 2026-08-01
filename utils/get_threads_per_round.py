
def get_threads_per_round(device: torch.device):
    if not isinstance(device, torch.device):
        device = torch.device(device)

    if device.type == "cuda":
        idx = device.index
        if idx is None:
            idx = torch.cuda.current_device()

        prop = torch.cuda.get_device_properties(idx)
        threads_per_round = (
            prop.multi_processor_count * prop.max_threads_per_multi_processor
        )
    else:
        _CPU_GRAIN_SIZE = 32768
        threads_per_round = _CPU_GRAIN_SIZE

    return threads_per_round

