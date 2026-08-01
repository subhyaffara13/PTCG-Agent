
def update_cb_config_after_cache_creation(
    cb_config: ContinuousBatchingConfig,
    num_blocks: int,
    max_batch_tokens: int,
    use_prefix_sharing: bool,
) -> None:
    """Updates the continuous batching config with the concrete values inferred during the creation of the cache."""
    # Memoize concrete values
    cb_config.num_blocks = num_blocks
    cb_config.max_batch_tokens = max_batch_tokens
    # Cap the number of max requests per batch to the max tokens per batch
    cb_config.max_requests_per_batch = min(cb_config.max_requests_per_batch, max_batch_tokens)
    # And if there is no prefix sharing, we can cap the number of request per batch (1 request = 1 block at least)
    if not use_prefix_sharing:
        cb_config.max_requests_per_batch = min(cb_config.max_requests_per_batch, num_blocks)

