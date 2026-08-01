
def _runtime_compute_coordinate_on_dim_impl(full_mesh: torch.Tensor, index: int) -> int:
    rank = torch.distributed.get_rank()
    mesh = DeviceMesh._get_mesh_tensor_from_full_mesh(full_mesh)
    mesh_coords = DeviceMesh._compute_coordinates_from_mesh(mesh, rank)
    if mesh_coords is None:
        raise AssertionError
    return mesh_coords[index]

