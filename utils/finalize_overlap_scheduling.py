from typing import Any

def finalize_overlap_scheduling(
    gm: fx.GraphModule,
    collective_info: dict[fx.Node, CollectiveInfo],
    scheduled: OrderedSet[fx.Node],
    *,
    collective_bucketing: bool = False,
    insert_overlap_deps: bool = False,
    max_bucket_memory_gb: float = 2.0,
    max_coll_distance: int = 1000,
    region_of: dict[fx.Node, Any] | None = None,
    bucket_exposed_first: bool | None = None,
    bucket_only_internode_comms: bool = False,
    bucket_mode: BucketMode | None = None,
) -> None:
    """
    Finalize overlap scheduling by applying deps, inlining fusions, and optionally bucketing.

    This is the main entry point for post-scheduling graph transformations:
    1. Bucket collectives (if collective_bucketing=True)
    2. Inline fusion regions back to original nodes
    3. Transfer deps from erased nodes to replacements
    4. Apply topological sort and effect tokens

    Args:
        gm: The graph module to modify
        collective_info: Dict mapping collective start nodes to their CollectiveInfo
        scheduled: Ordered set of scheduled nodes
        collective_bucketing: Whether to bucket collectives
        insert_overlap_deps: Whether to insert effect tokens for overlap deps
        max_bucket_memory_gb: Maximum memory for a bucket in GB
        max_coll_distance: Maximum distance for bucketing candidates
        region_of: Optional dict mapping module nodes to FusionRegions
    """
    bucketer = OverlapPreservingBucketer(
        graph=gm.graph,
        collective_info=collective_info,
        scheduled=scheduled,
        max_bucket_memory_gb=max_bucket_memory_gb,
        max_coll_distance=max_coll_distance,
        insert_overlap_deps=insert_overlap_deps,
        collective_bucketing=collective_bucketing,
        bucket_exposed_first=bucket_exposed_first,
        bucket_only_internode_comms=bucket_only_internode_comms,
        region_of=region_of,
        bucket_mode=bucket_mode,
    )
    bucketer.bucket_collectives()

