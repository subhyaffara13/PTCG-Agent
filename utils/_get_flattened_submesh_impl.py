
def _get_flattened_submesh_impl(mesh: DeviceMesh, mesh_dims: list[int]) -> DeviceMesh:
    from torch.distributed.tensor._redistribute import (
        _get_flattened_mesh_by_layout_impl,
    )

    result = _get_flattened_mesh_by_layout_impl(mesh, tuple(mesh_dims))
    if result is None:
        raise ValueError(f"No flattened mesh found for mesh_dims={mesh_dims} on {mesh}")
    return result

