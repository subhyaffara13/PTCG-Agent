
def _get_flattened_submesh(mesh: DeviceMesh, mesh_dims: list[int]) -> DeviceMesh:
    return _get_flattened_submesh_impl(mesh, mesh_dims)

