
def aggregate_stats(
    model: torch.nn.Module,
    mem_tracker: MemTracker,
    runtime_estimator: RuntimeEstimator,
    sac_estimator: SACEstimator,
    dev: torch.device,
) -> ModuleInfo:
    """
    Collect modulewise stats for a given model, including memory, runtime, and AC tradeoff stats.

    Args:
        model: nn.Module object
        runtime_estimator: RuntimeEstimator object with runtime stats
        mem_tracker: MemTracker object with memory stats
        sac_estimator: SACEstimator object with AC tradeoff stats
        dev: device the model was run on (used to extract memory stats from MemTracker)

    Returns:
        ModuleInfo: A dictionary with module order and module stats.
    """

    # Memory stats
    mod_mem_stats: dict[torch.nn.Module, _ModMemStats] = dict(
        copy.deepcopy(mem_tracker.memory_tracking)
    )

    # Runtime stats
    mod_runtime_stats: dict[str, ModRuntime] = {
        fqn: {"fw": v["fw"], "bw": v["bw"]}
        for fqn, v in runtime_estimator.mod_runtimes.items()
    }

    # Module order
    mod_order: ModOrder = {
        "fw_pre_order": list(runtime_estimator.mod_fw_pre_order),
        "bw_pre_order": list(runtime_estimator.mod_bw_pre_order),
        "fw_post_order": list(runtime_estimator.mod_fw_post_order),
        "bw_post_order": list(runtime_estimator.mod_bw_post_order),
    }

    # Selective Activation Checkpointing stats
    sac_estimator.pwlf_sac_tradeoff_curve()
    mod_sac_tradeoff_stats: dict[str, SACTradeOffStats] = copy.deepcopy(
        sac_estimator.sac_mod_tradeoff_stats
    )

    module_info: ModuleInfo = {
        "mod_order": mod_order,
        "mod_stats": [],
    }

    for mod in model.modules():
        if mod_mem_stat := mod_mem_stats.get(mod):
            if tradeoff_stats := mod_sac_tradeoff_stats.get(mod_mem_stat.mod_fqn):
                sac_runtime = tradeoff_stats.sac_runtime
                sac_memory = tradeoff_stats.sac_memory
                n_segments = tradeoff_stats.n_segments
                slopes = tradeoff_stats.slopes
                intercepts = tradeoff_stats.intercepts
                breakpoints = tradeoff_stats.fit_breaks
                tradeoff_curve = tradeoff_stats.tradeoff_curve
                is_leaf = False
            else:
                sac_runtime = sac_memory = n_segments = 0
                slopes = intercepts = breakpoints = []
                tradeoff_curve: OrderedDict[float, float] = OrderedDict()  # type: ignore[no-redef]
                is_leaf = True
            mod_stat: ModStats = {
                "fqn": mod_mem_stat.mod_fqn,
                "param_per_module": mod_mem_stat.parameter_mem,
                "grad_per_module": mod_mem_stat.parameter_mem,
                "grad_total": mod_mem_stat.snapshots[_ModState.PRE_BW][-1][dev][
                    _MemRefType.GRAD
                ],
                "act_fw_per_module": max(
                    0,
                    mod_mem_stat.snapshots[_ModState.POST_FW][-1][dev][_MemRefType.ACT]
                    - mod_mem_stat.snapshots[_ModState.PRE_FW][-1][dev][_MemRefType.ACT]
                    - mod_mem_stat.output_mem,
                ),
                "act_bw_per_module": max(
                    0,
                    mod_mem_stat.snapshots[_ModState.PEAK_BW][-1][dev][_MemRefType.ACT],
                ),
                "act_grad_per_module": (
                    mod_mem_stat.snapshots[_ModState.PEAK_BW][-1][dev][_MemRefType.TEMP]
                    - mod_mem_stat.snapshots[_ModState.PRE_BW][-1][dev][
                        _MemRefType.TEMP
                    ]
                ),
                "act_total": mod_mem_stat.snapshots[_ModState.POST_FW][-1][dev][
                    _MemRefType.ACT
                ],
                "input_per_module": mod_mem_stat.input_mem,
                "output_per_module": mod_mem_stat.output_mem,
                "fw_runtime_per_module": mod_runtime_stats[mod_mem_stat.mod_fqn]["fw"],
                "bw_runtime_per_module": mod_runtime_stats[mod_mem_stat.mod_fqn]["bw"],
                "is_leaf": is_leaf,
                "sac_runtime": sac_runtime,
                "sac_memory": sac_memory,
                "n_segments": n_segments,
                "slopes": slopes,
                "intercepts": intercepts,
                "breakpoints": breakpoints,
                "tradeoff_curve": tradeoff_curve,
            }
            module_info["mod_stats"].append(mod_stat)

    return module_info

