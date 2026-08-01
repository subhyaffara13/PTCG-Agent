
def _get_local_box(tensor: DTensor) -> tuple[torch.Size, torch.Size]:
    device_mesh = tensor.device_mesh
    coord = device_mesh.get_coordinate()
    if coord is None:
        raise AssertionError
    return _get_box_for(tensor, coord[0])

