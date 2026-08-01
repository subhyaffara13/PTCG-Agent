
def _init_default_mesh(
    mesh_dim_names: tuple[str, ...] | None = None,
) -> DeviceMesh:
    """Default to global CUDA mesh if possible else global CPU mesh."""
    if not dist.distributed_c10d.is_initialized():
        dist.distributed_c10d.init_process_group()
    default_pg = dist.distributed_c10d._get_default_group()
    device = torch._C._get_accelerator()
    mesh = init_device_mesh(
        device.type,
        mesh_shape=(default_pg.size(),),
        mesh_dim_names=mesh_dim_names,
    )
    return mesh

