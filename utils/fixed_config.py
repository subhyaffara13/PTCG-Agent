
def fixed_config(config, filename, triton_meta, inductor_meta):
    """
    Used when the configuration is already decided at compile time
    """
    config = {**config}
    return cached_autotune(
        None,
        [triton.Config(config, **_pop_config_kwargs(config))],
        triton_meta=triton_meta,
        inductor_meta=inductor_meta,
        heuristic_type=HeuristicType.FIXED,
        filename=filename,
    )

