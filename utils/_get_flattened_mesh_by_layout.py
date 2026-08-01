
def _get_flattened_mesh_by_layout(
    mesh: DeviceMesh, mesh_dims: tuple[int, ...]
) -> DeviceMesh | None:
    """
    Query for an explicitly created flattened mesh using layout comparison.

    When tracing with compile_on_one_rank, delegates to a custom op so the
    flattened mesh appears as a call_function node derived from mesh (a graph
    input) rather than as a get_attr constant holding an unpicklable
    ProcessGroup.
    """
    if _are_we_tracing() and torch.distributed.config.compile_on_one_rank:
        # Pre-check: the custom op can't return None (torch.library doesn't
        # support Optional opaque return types), so guard here first.
        if _get_flattened_mesh_by_layout_impl(mesh, mesh_dims) is None:
            return None
        from torch.distributed._ops import device_mesh as _  # noqa: F401

        return torch.ops.device_mesh._get_flattened_submesh(mesh, list(mesh_dims))

    return _get_flattened_mesh_by_layout_impl(mesh, mesh_dims)

