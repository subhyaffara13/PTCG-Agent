
def shard_dim_alltoall(input, gather_dim, shard_dim, mesh, mesh_dim):
    if mesh.device_type == "cpu" and local_tensor_mode() is None:
        # Gloo does not support alltoall, so falling back to allgather + chunk
        warning_once(
            logger,
            "CPU process group does not support alltoall yet, falling back with allgather + chunk!",
        )
        out = funcol.all_gather_tensor(input, gather_dim, (mesh, mesh_dim))
        if isinstance(out, funcol.AsyncCollectiveTensor):
            # stick to the same behavior for the alltoall case, remove this once we enable alltoall async
            out = out.wait()
        from torch.distributed.tensor.placement_types import Shard

        out = Shard._custom_chunk(out, mesh.size(mesh_dim), dim=shard_dim)[
            mesh.get_local_rank(mesh_dim)
        ]
        return out.contiguous()

    group = funcol._resolve_group((mesh, mesh_dim))
    # TODO: enable async op for shard_dim_alltoall
    return torch.ops._dtensor.shard_dim_alltoall(
        input, gather_dim, shard_dim, funcol._group_or_group_name(group)
    )

