
def _get_submesh_impl(mesh: DeviceMesh, mesh_dims: list[int]) -> DeviceMesh:
    all_dim_names = mesh._mesh_dim_names
    if all_dim_names is None:
        raise ValueError(f"Cannot slice mesh without dim names: {mesh}")
    dim_names = tuple(all_dim_names[i] for i in mesh_dims)
    if len(dim_names) == 1:
        return mesh[dim_names[0]]
    return mesh[dim_names]

