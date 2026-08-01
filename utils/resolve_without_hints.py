
def resolve_without_hints(cb_config: ContinuousBatchingConfig) -> None:
    """Fills any remaining unset/sentinel attribute with a fallback default."""
    if cb_config.max_requests_per_batch is None:
        cb_config.max_requests_per_batch = FALLBACK_DEFAULTS["max_requests_per_batch"]
    if cb_config.max_blocks_per_request is None:
        cb_config.max_blocks_per_request = FALLBACK_DEFAULTS["max_blocks_per_request"]
    if cb_config.q_padding_interval_size == 0:
        cb_config.q_padding_interval_size = FALLBACK_DEFAULTS["q_padding_interval_size"]
    if cb_config.kv_padding_interval_size == 0:
        cb_config.kv_padding_interval_size = FALLBACK_DEFAULTS["kv_padding_interval_size"]
    if cb_config.max_cached_graphs == 0:
        cb_config.max_cached_graphs = FALLBACK_DEFAULTS["max_cached_graphs"]

