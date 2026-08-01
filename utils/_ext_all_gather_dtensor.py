
def _ext_all_gather_dtensor(
    tensor: DTensor,
    parent_mesh: DeviceMesh | None,
    fsdp_extension: FSDPExtensions | None = None,
) -> torch.Tensor:
    all_gather_dtensor_fn = (
        fsdp_extension.all_gather_dtensor
        if fsdp_extension is not None
        else _all_gather_dtensor
    )
    return all_gather_dtensor_fn(tensor, parent_mesh)

