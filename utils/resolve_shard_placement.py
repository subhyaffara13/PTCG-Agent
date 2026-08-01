
def resolve_shard_placement(
    result: ShardPlacementFnResult,
    default_mesh_info: FSDPMeshInfo,
) -> ShardPlacementResult:
    """Resolve the shard_placement_fn result to a ShardPlacementResult.

    Handles different input types and applies defaults:
    - None: Use default sharding (Shard(0)) on default mesh
    - Shard: Use specified shard dimension on default mesh
    - ShardPlacementResult: Use as-is

    Args:
        result: The return value from shard_placement_fn, or None if no fn provided.
        default_mesh_info: The default FSDPMeshInfo to use if not specified.

    Returns:
        A ShardPlacementResult with placement and mesh_info.
    """
    if result is None:
        return ShardPlacementResult(placement=None, mesh_info=default_mesh_info)
    if isinstance(result, Shard):
        return ShardPlacementResult(placement=result, mesh_info=default_mesh_info)
    if isinstance(result, ShardPlacementResult):
        return result
    raise ValueError(f"Invalid shard_placement_fn result: {result}")

