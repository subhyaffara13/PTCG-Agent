
def resolve_max_memory_percent(cb_config: ContinuousBatchingConfig, has_logit_processors: bool) -> None:
    if cb_config.max_memory_percent is None:
        cb_config.max_memory_percent = 0.8 if has_logit_processors else 0.9

