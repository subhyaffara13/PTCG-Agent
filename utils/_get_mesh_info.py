
def _get_mesh_info(
    mesh: "DeviceMesh",
    dp_mesh_dims: "DataParallelMeshDims | None" = None,
) -> "DataParallelMeshInfo":
    """
    Get the appropriate mesh info for the given mesh.

    When ``dp_mesh_dims`` is provided, extracts the DP submesh from the
    full SPMD mesh and returns FSDPMeshInfo, HSDPMeshInfo, or DDPMeshInfo
    with ``dp_mesh_dims`` set and ``is_spmd_mesh`` as True.

    Returns FSDPMeshInfo for 1D mesh, HSDPMeshInfo for 2D mesh.
    """
    if dp_mesh_dims is not None:
        return _get_mesh_info_from_named_dims(mesh, dp_mesh_dims)
    if mesh.ndim == 1:
        return FSDPMeshInfo(mesh, shard_mesh_dim=0)
    else:
        return HSDPMeshInfo(mesh, shard_mesh_dim=1, replicate_mesh_dim=0)

