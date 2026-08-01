
def schedule_overlap_bucketing_from_inductor_configs(
    gm: torch.fx.GraphModule,
) -> torch.fx.GraphModule:
    """Schedule nodes to maximize compute-collective overlap using inductor configs.

    Reads configuration from torch._inductor.config.aten_distributed_optimizations
    and calls schedule_overlap_bucketing with those settings.
    """
    if not any(is_wait_tensor(n) for n in gm.graph.nodes):
        return gm

    from torch._inductor import config

    dist_opts = config.aten_distributed_optimizations

    kwargs: dict[str, object] = {}

    config_keys = (
        "collective_bucketing",
        "max_compute_pre_fetch",
        "custom_runtime_estimation",
        "insert_overlap_deps",
        "collective_estimator",
        "compute_estimator",
        "max_memory_increase_gb",
        "max_memory_increase_ratio",
        "compute_overlap_multipler",
        "max_in_flight_gb",
        "max_coll_distance",
        "log_final_collectives_estimations",
        "bucket_exposed_first",
        "bucket_only_internode_comms",
        "enable_fusion_regions",
        "prioritize_bucketing_during_scheduling",
        "bucket_mode",
    )
    for key in config_keys:
        if (val := getattr(dist_opts, key, None)) is not None:
            kwargs[key] = val

    return schedule_overlap_bucketing(gm, **kwargs)  # type: ignore[arg-type]

