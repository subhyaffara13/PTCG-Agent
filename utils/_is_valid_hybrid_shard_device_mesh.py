
def _is_valid_hybrid_shard_device_mesh(device_mesh: DeviceMesh) -> bool:
    return isinstance(device_mesh, DeviceMesh) and device_mesh.ndim == 2

