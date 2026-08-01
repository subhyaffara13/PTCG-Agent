
def _convert_to_global_idxs(
    local_idx: torch.Tensor,
    global_shape: torch.Size,
    device_mesh: "torch.distributed.device_mesh.DeviceMesh",
    placements: tuple[Placement, ...],
    dim: int | None,
) -> tuple[int, torch.Tensor]:
    """Convert local indices to global indices."""
    local_shape, global_offset = compute_local_shape_and_global_offset(
        global_shape, device_mesh, placements
    )

    if dim is None:
        # Convert flat local index → flat global index using arithmetic ops
        # instead of torch.unravel_index, which doesn't support SymInt shapes.
        gathered_idxs = torch.zeros_like(local_idx)
        remaining = local_idx
        for i in range(len(local_shape)):
            local_stride = reduce(operator.mul, local_shape[i + 1 :], 1)
            global_stride = reduce(operator.mul, global_shape[i + 1 :], 1)
            coord = remaining // local_stride
            remaining = remaining % local_stride
            gathered_idxs = gathered_idxs + (coord + global_offset[i]) * global_stride
        gather_dim = 0
    else:
        gather_dim = dim
        gathered_idxs = local_idx + global_offset[dim]
    return gather_dim, gathered_idxs

