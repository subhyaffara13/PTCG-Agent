
def is_tensor_dim_sharded(spec: DTensorSpec, dim: int) -> bool:
    """Return True if tensor dim is sharded."""
    return any(_is_shard_like(p) and p.dim == dim for p in spec.placements)

