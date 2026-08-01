
def cooperative_reduction(
    size_hints,
    reduction_hint,
    triton_meta,
    filename,
    inductor_meta,
):
    inductor_meta = {} if inductor_meta is None else inductor_meta
    inductor_meta["reduction_hint"] = reduction_hint
    if inductor_meta.get("no_x_dim"):
        size_hints["x"] = 1

    # Cooperative reductions currently only support a single reduction dimension.
    assert len(size_hints) == 2, (
        "Cooperative reductions don't support tiling reduction dims"
    )
    xnumel, rnumel = size_hints["x"], size_hints["r0_"]

    # Note that we must never create more CTAs than there are SMs, because we
    # depend on synchronizing between the CTAs in x_grid_barrier, and that will
    # deadlock if some of the CTAs are not running. In order to maximize use of
    # the GPU, we want to create as many CTAs as possible, while keeping things
    # in powers of 2.
    target = last_power_of_2(triton_meta["device"].multi_processor_count)
    split = max(1, min((rnumel, target // xnumel, TRITON_MAX_RSPLIT)))
    if inductor_meta["persistent_reduction"]:
        configs = _persistent_reduction_configs(
            {"x": xnumel, "r0_": rnumel // split},
            reduction_hint,
            inductor_meta,
            triton_meta,
        )
    else:
        configs = _reduction_configs(
            size_hints={"x": xnumel, "r0_": rnumel // split},
            inductor_meta=inductor_meta,
            triton_meta=triton_meta,
        )
    for config in configs:
        config.kwargs["RSPLIT"] = split
    # TODO(jansel): add more configs in max_autotune

    configs = _maybe_filter_configs_for_tma_restrictions(inductor_meta, configs)
    configs = filter_reduction_configs_for_determinism(inductor_meta, configs)
    return cached_autotune(
        size_hints,
        configs=configs,
        triton_meta=triton_meta,
        inductor_meta=inductor_meta,
        heuristic_type=HeuristicType.REDUCTION,
        filename=filename,
    )

