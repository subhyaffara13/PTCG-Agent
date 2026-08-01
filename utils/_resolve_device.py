
def _resolve_device(device_mesh: DeviceMesh) -> torch.device:
    device_type = device_mesh.device_type
    device_handle = _get_device_handle(device_type)
    if device_handle is None:
        raise AssertionError
    device_idx = device_mesh.get_rank() % device_handle.device_count()

    @maybe_run_for_local_tensor
    def get_device(device_idx):
        return torch.device(f"{device_type}:{device_idx:d}")

    return get_device(device_idx)

