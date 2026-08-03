from typing import Callable

def schedule_overlap_bucketing(
    gm: torch.fx.GraphModule,
    max_in_flight_gb: float = 5,
    max_compute_pre_fetch: int = 200,
    collective_bucketing: bool = False,
    insert_overlap_deps: bool = False,
    compute_overlap_multipler: float = 1.0,
    max_coll_distance: int = 200,
    custom_runtime_estimation: Callable[[fx.Node, int | None], float | None]
    | None = None,
    collective_estimator: Literal["analytical", "benchmark"] = "analytical",
    compute_estimator: Literal["analytical", "benchmark"] = "benchmark",
    max_memory_increase_gb: float | None = 1.0,
    max_memory_increase_ratio: float | None = 0.05,
    log_final_collectives_estimations: bool = False,
    bucket_exposed_first: bool | None = None,
    enable_fusion_regions: bool = False,
    bucket_only_internode_comms=False,
    prioritize_bucketing_during_scheduling: bool = True,
    max_off_bucket_gb: float | None = 0.5,
    bucket_mode: BucketMode | None = None,
) -> torch.fx.GraphModule:
    """Schedule nodes to maximize compute-collective overlap.

    Args:
        gm: Input graph module to optimize.
        max_in_flight_gb: Maximum GB of concurrent collective data. Too much in flight memory
            can cause memory fragmentation within the CUDA Caching Allocator.
        max_compute_pre_fetch: Maximum mm nodes to pre fetch. Note: should already be limited by max_in_flight_gb and
            max_memory_increase_gb
        collective_bucketing: Enable overlap-preserving collective bucketing.
        insert_overlap_deps: Insert overlap dependencies using control deps operator. This should only be used if
            compiling with inductor, or for subsequent passes before removing the ops prior to execution.
        compute_overlap_multipler: Scale factor for compute time used to hide collectives. This can be used
            to address over or under aggressive overlapping.
        max_coll_distance: Maximum pre fetch or bucketing candidates. Mainly intended for compile time
        custom_runtime_estimation: Override runtime estimation for specific nodes. Called as
            custom_runtime_estimation(node, override_size) -> float | None. To pass pre-computed
            estimations, wrap a dict: lambda node, _: estimations.get(node).
        collective_estimator: Method for estimating collective runtime. "analytical" uses bandwidth formulas,
            "benchmark" uses CUDA events with power-of-2 rounding and interpolation.
        compute_estimator: Method for estimating compute (ATen op) runtime. "analytical" uses roofline model
            estimates (deterministic, no GPU sync), "benchmark" uses GPU benchmarking (more accurate).
        max_memory_increase_gb: Maximum GB increase above baseline memory (absolute cap). If None, no absolute limit.
        max_memory_increase_ratio: Maximum increase as ratio of baseline peak memory. If None, no ratio limit.
            Uses minimum of absolute and ratio limits when both are specified.
        enable_fusion_regions: Enable fusion region detection and cost estimation for fusible ops.
        bucket_mode: Bucketing mode for grouping collectives.
    """
    if not any(is_wait_tensor(n) for n in gm.graph.nodes):
        return gm

    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "overlap_scheduling_graph_before",
            "encoding": "string",
        },
        payload_fn=lambda: gm.print_readable(False),
    )
    ret = OverlapScheduler(
        gm,
        compute_overlap_multipler=compute_overlap_multipler,
        max_in_flight_gb=max_in_flight_gb,
        max_coll_distance=max_coll_distance,
        max_compute_pre_fetch=max_compute_pre_fetch,
        custom_runtime_estimation=custom_runtime_estimation,
        collective_bucketing=collective_bucketing,
        insert_overlap_deps=insert_overlap_deps,
        collective_estimator=collective_estimator,
        compute_estimator=compute_estimator,
        max_memory_increase_gb=max_memory_increase_gb,
        max_memory_increase_ratio=max_memory_increase_ratio,
        log_final_collectives_estimations=log_final_collectives_estimations,
        bucket_exposed_first=bucket_exposed_first,
        enable_fusion_regions=enable_fusion_regions,
        bucket_only_internode_comms=bucket_only_internode_comms,
        prioritize_bucketing_during_scheduling=prioritize_bucketing_during_scheduling,
        max_off_bucket_gb=max_off_bucket_gb,
        bucket_mode=bucket_mode,
    ).run()
    trace_structured(
        "artifact",
        metadata_fn=lambda: {
            "name": "overlap_scheduling_graph_after",
            "encoding": "string",
        },
        payload_fn=lambda: ret.print_readable(False),
    )
    return ret

