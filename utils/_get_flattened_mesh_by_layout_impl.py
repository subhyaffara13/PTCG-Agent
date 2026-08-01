
def _get_flattened_mesh_by_layout_impl(
    mesh: DeviceMesh, mesh_dims: tuple[int, ...]
) -> DeviceMesh | None:
    """
    Query for an explicitly created flattened mesh using layout comparison.

    Searches root_mesh._flatten_mapping for a mesh whose layout matches
    the expected flattened layout for the given dims. Pure Python layout math.
    """
    root_mesh = mesh._get_root_mesh()
    mesh_dim_names = mesh.mesh_dim_names

    if mesh_dim_names is None:
        return None

    # Convert mesh dim indices to dim names
    dim_names = tuple(mesh_dim_names[i] for i in mesh_dims)

    # Compute expected layout WITHOUT creating a submesh (avoids tracing issues)
    # _get_slice_mesh_layout does pure layout math, no tensor operations
    sliced_layout = mesh._get_slice_mesh_layout(dim_names)
    expected_layout = sliced_layout.coalesce()
    if len(expected_layout) > 1:
        expected_layout = expected_layout.nest()

    # Search existing flattened meshes by comparing layouts
    for flattened_mesh in root_mesh._flatten_mapping.values():
        if flattened_mesh._layout == expected_layout:
            return flattened_mesh

    return None

