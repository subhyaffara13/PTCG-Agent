
def _get_mesh_info_from_named_dims(
    mesh: "DeviceMesh",
    dp_mesh_dims: "DataParallelMeshDims",
) -> "DataParallelMeshInfo":
    shard_names = dp_mesh_dims.shard_names
    replicate_names = dp_mesh_dims.replicate_names

    def _get_submesh(names: tuple[str, ...]) -> "DeviceMesh":
        if len(names) == 1:
            return mesh[names[0]]
        # Flatten multi-dim submesh into a single dim so FSDP's internal
        # logic (which expects one shard and/or one replicate dim) works
        # unchanged. This creates a new 1D DeviceMesh and ProcessGroup.
        return mesh[names]._flatten("_".join(names))

    if len(shard_names) == 0:  # DDP
        dp_mesh = _get_submesh(replicate_names)
        return DDPMeshInfo(
            dp_mesh,
            replicate_mesh_dim=0,
            dp_mesh_dims=dp_mesh_dims,
            spmd_mesh=mesh,
        )
    if len(replicate_names) == 0:  # FSDP
        dp_mesh = _get_submesh(shard_names)
        return FSDPMeshInfo(
            dp_mesh,
            shard_mesh_dim=0,
            dp_mesh_dims=dp_mesh_dims,
            spmd_mesh=mesh,
        )
    # HSDP
    shard_mesh = _get_submesh(shard_names)
    replicate_mesh = _get_submesh(replicate_names)
    dp_mesh = DeviceMesh._concatenate([replicate_mesh, shard_mesh])
    return HSDPMeshInfo(
        dp_mesh,
        shard_mesh_dim=1,
        replicate_mesh_dim=0,
        dp_mesh_dims=dp_mesh_dims,
        spmd_mesh=mesh,
    )

