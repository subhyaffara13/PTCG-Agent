from typing import Any

def shard_order_to_placement(shard_order, mesh):
    """convert shard_order to placement with only Replicate() and Shard()"""
    placements: list[Any] = [Replicate() for _ in range(mesh.ndim)]
    if shard_order is not None:
        for entry in shard_order:
            tensor_dim = entry.tensor_dim
            mesh_dims = entry.mesh_dims
            for mesh_dim in mesh_dims:
                placements[mesh_dim] = Shard(tensor_dim)
    return tuple(placements)

